import pandas as pd
import sqlite3

# This file is responsible for managing the database schema,
# Responsibilities:
# Discover existing tables in the database
# Represent table schemas as structured objects (table, columns, types)
# Compare schemas to determine compatibility (append vs create)
# Provide schema information to other components (e.g., Query Service, LLM)

#Function that dictates whether data from pandas table is similar
#to existing data.

#Function that retrieves all tables and provides their schema in a readable way.
#Schemas will be provided as [table_name, [columns], [types]]

#
