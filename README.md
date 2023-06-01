# Natural Language to SQL Query Converter



This repository contains a project that allows you to convert natural language questions into SQL queries and returns results using the power of OpenAI's GPT model and Python.

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

## Introduction

This project uses OpenAI's GPT model to interpret natural language and generate SQL queries. Once the SQL query is generated, it is executed on the specified database, and the result is returned.

The goal of this project is to make database querying accessible to non-programmers and reduce the effort needed to extract insights from data.

## Features

- **Natural Language Processing**: Uses OpenAI's GPT model for natural language understanding.
- **SQL Query Generation**: Generates SQL queries from natural language input.
- **Database Querying**: Executes SQL queries on a database and returns results.

## Installation

1. Clone this repository and Navigate to the NLP_to_SQL folder.

    ```
    git clone [https://github.com/username/nl-to-sql.git](https://github.com/NSR9/GPT_Projects.git)
    ```
2. Install the necessary dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Set up your database connection and OpenAI API key in the `main.py` file.

2. Run the main script:

    ```
    python3 main.py
    ```

3. Enter your natural language query when prompted.

## Contributing

Contributions are always welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for ways to get started.

Please adhere to this project's `code of conduct`.

## License

This project is [MIT](LICENSE) licensed.
