import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy import text
 

"""
The below DataProcessor class handles all the data processing operations:

1. Read the data from the files with different file formats in to a pandas dataframe.
2. Process the dataframe and insert the data into an sql table.
3. Define and process prompts for OpenAI API to generate SQL queries.

"""
class DataProcessor():
 def __init__(self, sql_engine):
  self.engine = sql_engine

# This function is setup to read data from a file and convert it into a Pandas Dataframe.

 def read_file_into_df(self, file_path):
    # Open the file using a context manager
    with open(file_path, 'r') as file:
        # Split the file name into name and extension
        x, file_extension = os.path.splitext(file_path)
        # defining the table name
        table_name = x.split('/')[-1]
        # Convert extension to lowercase to avoid case issues
        file_extension = file_extension.lower()

        # Check the file type by extension and read the file using the appropriate pandas function
        if file_extension == '.csv':
            # If the file is a CSV file, read it using pandas read_csv function
            df = pd.read_csv(file)
        elif file_extension == '.xlsx':
            # If the file is an XLSX file, read it using pandas read_excel function
            # The engine 'openpyxl' is used to handle xlsx files
            df = pd.read_excel(file, engine='openpyxl')
        elif file_extension == '.json':
            # If the file is a JSON file, read it using pandas read_json function
            df = pd.read_json(file)
        elif file_extension == '.txt':
            # If the file is a TXT file, read it as a CSV file with tab ('\t') as separator
            # This assumes that the text file is tab-separated
            df = pd.read_csv(file, sep="\t")
        else:
            # If the file type is none of the above, raise an error
            raise ValueError(f'Unsupported file type: {file_extension}')
            
    # Return the data frame
    return df, table_name
 


# This function takes the data frame and ports the data into a SQL Database in RAM(This is customizable)
 def df_to_sql(self, df, table_name):
     # Creating the connection to the database
     """Convert a pandas dataframe to a database.
        Args:
            df (dataframe): pd.DataFrame which is to be converted to a database
            table_name (string): Name of the table within the database
        Returns:
            engine: SQLAlchemy engine object
    """
     data_sql_table  = df.to_sql(name=table_name, con=self.engine)
     query = f"Select * from {table_name}"
     with self.engine.connect() as conn:
       result = conn.execute(text(query))
     # Use the below three lines to check and list the table names in the database.   
      #  inspector = inspect(self.engine)
      #  table_names = inspector.get_table_names()
      #  print("#####" + "\n \n" + str(table_names) + "\n \n")
       print("data ported into SQL")




# This function builds the table definition prompt to set the pre-context for GPT.
 def define_table_definition_prompt(self, df, table_name):
    """This function creates a prompt for the OpenAI API to generate SQL queries.

    Args:
        df (dataframe): pd.DataFrame object to automtically extract the table columns
        table_name (string): Name of the table within the database

        Returns: string containing the prompt for OpenAI
    """
    table_definition_prompt = """### Sqlite SQL table with the following properties:
     #
     {}({})
     #
     """.format(table_name, ",".join(str(col) for col in df.columns))
    return table_definition_prompt



# This function builds the query prompt based on the user prompt. 
 def get_query_from_user_prompt(self):
    """Ask the user what they want to know about the data.

    Returns:
        string: User input
    """
    user_prompt = input("Ask a question (or) details You would Like to know about the data:")
    query_prompt = f"""## Here is a Question to answer: {user_prompt}\n SELECT"""
    return query_prompt



# This function builds the final prompt combined with user query prompt and pre-context prompt.
 def final_prompt_to_gpt(self, df, table_name, query_prompt):
    """Combine the fixed SQL prompt with the user query.

    Args:
        fixed_sql_prompt (string): Fixed SQL prompt
        user_query (string): User query

    Returns:
        string: Combined prompt
    """
    table_definition = self.define_table_definition_prompt(df, table_name)
    return table_definition + query_prompt
 







