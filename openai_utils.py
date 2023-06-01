import openai
from data_handler import DataProcessor
import sqlalchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy import text


"""
The GPTHandler class is designed by me to handle the responses generated by OpenAI's GPT (Generative Pre-trained Transformer) model. 
It serves as a bridge between the GPT model and a SQL database engine.

Here's a description of the class and its main components:

Attributes:

model: A string representing the GPT model to be used. In this case, it is set to "text-davinci-003".

temperature: A float value indicating the randomness of the generated responses. A higher temperature
             leads to more diverse but potentially less coherent responses.

max_tokens: An integer specifying the maximum number of tokens in the generated response.

frequency_penalty: A float value representing the penalty for high-frequency tokens. Higher values will 
                   make the model generate less repetitive responses.

presence_penalty: A float value indicating the penalty for using new tokens. Higher values encourage the
                  model to use a wider range of tokens.

engine: An SQL engine object used to connect to the database and execute SQL queries.

Methods:

get_gpt_response(prompt): Sends a prompt string to the GPT model and returns the response generated by the
   model. The prompt is passed as the prompt parameter, and the method uses the specified GPT model, temperature,
   max tokens, frequency penalty, and presence penalty for generating the response.

handle_gpt_response(response): Processes the GPT response and executes the generated SQL query using the 
   SQL engine. The response parameter is a dictionary containing the GPT response. The method extracts 
   the SQL query from the response, adds a "SELECT" keyword if necessary, and then executes the query 
   using the SQL engine. The method returns the query results as a list.Overall, the GPTHandler class 
   provides a convenient way to interact with the GPT model and execute SQL queries based on the generated
   responses. It encapsulates the logic of handling GPT responses and integrating them with an SQL engine,
   making it easier to use GPT for SQL-related tasks.
"""
# GPT response Handler Class
class GPTHandler(DataProcessor):
  def __init__(self, sql_engine):
    self.model = "text-davinci-003" 
    self.temperature = 0
    self.max_tokens = 150
    self.frequency_penalty = 0
    self.presence_penalty = 0
    self.engine = sql_engine
    
  def get_gpt_response(self, prompt):
    """
    Send the prompt to OpenAI

    Args:
        prompt (string): Prompt to send to OpenAI

    Returns:
        string: Response from OpenAI
    """
    gpt_response = openai.Completion.create(
        model=self.model,
        prompt=prompt,
        temperature=self.temperature,
        max_tokens=self.max_tokens,
        frequency_penalty=self.frequency_penalty,
        presence_penalty=self.presence_penalty,
        stop=['#', ';']
    )
    return gpt_response

  def handle_gpt_response(self, response):
    """
    Process the GPT response and execute the generated SQL query

    Args:
        response (dict): Response from OpenAI GPT

    Returns:
        list: Query results from executing the generated SQL query
    """
    query = response['choices'][0]['text']
    if query.startswith(" "):
        query = "SELECT" + query
    with self.engine.connect() as conn:
      query_results = conn.execute(text(query)).all()
    return query_results









