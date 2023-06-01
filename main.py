# Importing required libraries and modules
import os
import logging

import pandas as pd
import openai
from sqlalchemy import create_engine, inspect

# Importing classes from custom modules
from data_handler import DataProcessor
from openai_utils import GPTHandler

# Creating an SQL engine to connect to a temporary in-memory database
sql_engine = create_engine('sqlite:///:memory:', echo=False)

# Setting up logging and OpenAI API key
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
openai.api_key = "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"

if __name__ == "__main__":
    # Initializing DataProcessor and GPTHandler objects
    dataprocessor = DataProcessor(sql_engine)
    gpt_handler = GPTHandler(sql_engine)

    # Path of the file to be processed and queried. This path can be changed at any point. 
    filepath = "./data/sales_data_sample.csv"
  
    logging.info("Loading data...")
    # Reading the CSV file into a DataFrame and getting the table name
    df, table = dataprocessor.read_file_into_df(filepath)
    logging.info(f"Data Format: {df.shape}")

    logging.info("Converting to database...")
    # Converting the DataFrame to an SQL table in the in-memory database
    dataprocessor.df_to_sql(df, table)

    logging.info("Waiting for user input...")
    # Getting the user's query prompt
    query_prompt = dataprocessor.get_query_from_user_prompt()

    # Creating the final prompt to be sent to OpenAI GPT
    final_prompt = dataprocessor.final_prompt_to_gpt(df, table, query_prompt)
    logging.info(f"Final Prompt: {final_prompt}")

    logging.info("Sending to OpenAI...")
    # Getting the response from OpenAI GPT based on the final prompt
    gpt_response = gpt_handler.get_gpt_response(final_prompt)
    # Handling the GPT response and executing the generated SQL query
    response_with_results = gpt_handler.handle_gpt_response(gpt_response)
    logging.info(f"Result: {response_with_results}")
