# Queryable Database 
#### Built for EC530 Software Engineering Principles

### Overview

This is a framework for a queryable database once data is inserted inside.
The project uses the OpenAI LLM and an appropriate environment key must be placed to use.

The additional csv files inside the project are used as examples and used for unit testing.

To run the project, run main.py

### Design
The design of the system is as follows:

CSV Reader - Reads a file path and attempts to create a new table or update an existing one if enough headers are similar.

Schema Manager - Provides either similar tables for the csv reader, or the table schema to the query service to verify SQL queries. Also used for logging.

Query Service - Used as an intermediary between user input and the rest of the system, such as providing the natural language instructions to the LLM, and verifying it.

LLM Interface - Generates the prompt and uses the OpenAI API to respond with a SQL query that best matches the user input.

SQL Verifier - A safety measure ensuring that what the LLM provides is accurate and not malicious.
