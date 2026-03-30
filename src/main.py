import query_service
import csv_reader
from dotenv import load_dotenv
import os

#Main Code

#General Process:
#Query the user for inputting something (adding data, getting data, etc.)
#Use LLM to parse input into SQL commands
#Attempt to execute SQL commands on the database
#Return results to the user

#Configuration
load_dotenv()
DEBUG = os.getenv("DEBUG", "false").strip().lower() == "true"
print("Debug is on.\n")

if __name__ == "__main__":
    print("Type 'quit' to exit.")
    print("To input data, use the syntax: 'insert [path_name]'")
    print("To query data, use the syntax: 'query [query]'")

    while(True):
        user_input = input("\nEnter your command: ")
        print() #newline for prettiness
        if user_input.lower() == "quit":
            print("Exiting the program.")
            break

        elif user_input.lower().startswith("insert "):
            file_path = user_input[7:].strip()
            status = csv_reader.load_csv(file_path)
            if status == 200:
                print("CSV file loaded successfully.")
            else:
                print("Failed to load CSV file.")

        elif user_input.lower().startswith("query "):
            query = user_input[6:].strip()
            #Run the query and return results
            results = query_service.execute_command(query)
            #may be better in the future to have pretty print
            print(results)
        
        else:
            print("Not a recognized command.")
        
