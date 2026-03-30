import openai
import dotenv
import schema_manager

#Interface for LLM to generate SQL queries

#Generates query from user input.
def generate_query(user_input):
    #debuf purposes, skip ai for now and instead just assume query is given

    
    #Generates Prompt
    prompt_beginning = ""
    prompt = f"{prompt_beginning}\nUser Input: {user_input}\nSQL Query:"

    #TODO: LLM Call
    response = "" #change to ai call

    return response

schema = schema_manager.get_tables()

#Get a string ready for stringifying the table schemas.
schema_string = ""
index = 0
for table in schema:
    col_names = table[1]
    col_types = table[2]
    table_string = f"Table {index} name: {table[0]}. Columns: "
    
    for i in range(len(col_names)):
        table_string = table_string + f"{col_names[i]} with type {col_types[i]}, "

    schema_string = table_string[:-2] + f". End of Table {table[0]}. "
  
print(schema_string)

prompt = """

You are an AI managing 
"""
