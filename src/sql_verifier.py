import sqlglot
import sqlglot.expressions as exp
import schema_manager

def validate_query(query):
    # ── 1. Basic safety checks ────────────────────────────────────────────────
    if not query.strip().upper().startswith("SELECT"):
        print("DEBUG Query validation failed: Query must start with SELECT.")
        return False
    if ";" in query.strip().rstrip(";"):
        print("DEBUG Query validation failed: Query cannot contain semicolons.")
        return False
    if any(kw in query.upper() for kw in ("DROP", "DELETE", "INSERT", "UPDATE")):
        print("DEBUG Query validation failed: Query cannot contain DROP, DELETE, INSERT, or UPDATE.")
        return False

    # ── 2. Build schema lookup from get_tables() ──────────────────────────────
    # get_tables() returns: [ [table_name, [col_names], [col_dtypes]], ... ]
    raw_schemas = schema_manager.get_tables()

    # schema = { "table_name": { "col_name": "dtype", ... }, ... }
    schema = {}
    for table_name, col_names, col_dtypes in raw_schemas:
        schema[table_name.lower()] = {
            col.lower(): dtype.lower()
            for col, dtype in zip(col_names, col_dtypes)
        }

    # Numeric types — used for aggregate compatibility checks
    NUMERIC_TYPES = {"int", "integer", "bigint", "smallint", "float", "double",
                     "decimal", "numeric", "real", "number"}

    # ── 3. Parse SQL ──────────────────────────────────────────────────────────
    try:
        parsed = sqlglot.parse_one(query)
    except sqlglot.errors.ParseError as e:
        print(f"DEBUG Query validation failed: SQL parse error: {e}")
        return False

    # ── 4. Collect tables referenced in the query ─────────────────────────────
    # Builds alias map: { alias_or_tablename -> canonical_table_name }
    alias_map = {}
    for table_node in parsed.find_all(exp.Table):
        tname = table_node.name.lower()
        alias = table_node.alias.lower() if table_node.alias else tname
        if tname not in schema:
            print(f"DEBUG Query validation failed: Table '{tname}' does not exist.")
            return False
        alias_map[alias] = tname

    if not alias_map:
        print("DEBUG Query validation failed: No tables found in query.")
        return False

    # ── 5. Validate columns exist ─────────────────────────────────────────────
    for col_node in parsed.find_all(exp.Column):
        col_name = col_node.name.lower()
        table_ref = col_node.table.lower() if col_node.table else None

        if col_name == "*":
            continue  # SELECT * is always fine

        if table_ref:
            # Qualified column: alias.col or table.col
            if table_ref not in alias_map:
                print(f"DEBUG Query validation failed: Unknown table reference '{table_ref}'.")
                return False
            real_table = alias_map[table_ref]
            if col_name not in schema[real_table]:
                print(f"DEBUG Query validation failed: Column '{col_name}' not found in table '{real_table}'.")
                return False
        else:
            # Unqualified column: search all referenced tables
            found = any(col_name in schema[alias_map[a]] for a in alias_map)
            if not found:
                print(f"DEBUG Query validation failed: Column '{col_name}' not found in any referenced table.")
                return False

    # ── 6. Validate aggregate type compatibility ──────────────────────────────
    NUMERIC_AGGREGATES = {"sum", "avg"}

    for agg_node in parsed.find_all(exp.Anonymous):
        func_name = agg_node.name.lower()
        if func_name not in NUMERIC_AGGREGATES:
            continue
        for col_node in agg_node.find_all(exp.Column):
            col_name = col_node.name.lower()
            table_ref = col_node.table.lower() if col_node.table else None
            real_table = alias_map.get(table_ref) if table_ref else next(
                (alias_map[a] for a in alias_map if col_name in schema[alias_map[a]]), None
            )
            if real_table and col_name in schema[real_table]:
                dtype = schema[real_table][col_name]
                base_type = dtype.split("(")[0].strip()  # handles "varchar(255)" etc.
                if base_type not in NUMERIC_TYPES:
                    print(f"DEBUG Query validation failed: '{func_name.upper()}({col_name})' used on non-numeric type '{dtype}'.")
                    return False

    # Also check sqlglot-recognised aggregates (SUM, AVG as typed expressions)
    for agg_class in (exp.Sum, exp.Avg):
        for agg_node in parsed.find_all(agg_class):
            for col_node in agg_node.find_all(exp.Column):
                col_name = col_node.name.lower()
                table_ref = col_node.table.lower() if col_node.table else None
                real_table = alias_map.get(table_ref) if table_ref else next(
                    (alias_map[a] for a in alias_map if col_name in schema[alias_map[a]]), None
                )
                if real_table and col_name in schema[real_table]:
                    dtype = schema[real_table][col_name]
                    base_type = dtype.split("(")[0].strip()
                    if base_type not in NUMERIC_TYPES:
                        print(f"DEBUG Query validation failed: '{agg_class.__name__.upper()}({col_name})' used on non-numeric type '{dtype}'.")
                        return False

    # ── 7. Validate JOIN conditions ───────────────────────────────────────────
    for join_node in parsed.find_all(exp.Join):
        condition = join_node.args.get("on")
        if condition is None:
            # USING(...) clause — extract column name
            using = join_node.args.get("using")
            if using:
                for col_node in using if isinstance(using, list) else [using]:
                    col_name = col_node.name.lower() if hasattr(col_node, "name") else str(col_node).lower()
                    found_in = [t for t in alias_map.values() if col_name in schema[t]]
                    if len(found_in) < 2:
                        print(f"DEBUG Query validation failed: JOIN USING column '{col_name}' must exist in at least two tables.")
                        return False
            continue

        # ON clause: collect both sides of EQ conditions
        for eq_node in condition.find_all(exp.EQ):
            sides = [eq_node.left, eq_node.right]
            resolved = []
            for side in sides:
                if isinstance(side, exp.Column):
                    col_name = side.name.lower()
                    table_ref = side.table.lower() if side.table else None
                    if table_ref:
                        if table_ref not in alias_map:
                            print(f"DEBUG Query validation failed: Unknown table '{table_ref}' in JOIN condition.")
                            return False
                        real_table = alias_map[table_ref]
                        if col_name not in schema[real_table]:
                            print(f"DEBUG Query validation failed: Column '{col_name}' not in table '{real_table}' (JOIN condition).")
                            return False
                        resolved.append((real_table, col_name))
            # If both sides resolved, check type compatibility
            if len(resolved) == 2:
                (t1, c1), (t2, c2) = resolved
                dtype1 = schema[t1][c1].split("(")[0].strip()
                dtype2 = schema[t2][c2].split("(")[0].strip()
                if dtype1 != dtype2:
                    print(f"DEBUG Query validation failed: JOIN type mismatch: '{t1}.{c1}' ({dtype1}) vs '{t2}.{c2}' ({dtype2}).")
                    return False

    print("DEBUG Query validation passed.")
    return True
