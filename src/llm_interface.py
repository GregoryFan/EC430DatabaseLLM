import openai
import sql_verifier
import sqlite3

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


