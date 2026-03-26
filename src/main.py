import sql_verifier

#Main Code

#General Process:
#Query the user for inputting something (adding data, getting data, etc.)
#Use LLM to parse input into SQL commands
#Attempt to execute SQL commands on the database
#Return results to the user

if __name__ == "__main__":
    while(True):
        #Get user input.
        user_input = input("Type input: ")
        #break clause
        if user_input.lower() == "quit":
            print("Exiting program.")
            break

        #debug
        print(sql_verifier.validate_query(user_input))
    pass