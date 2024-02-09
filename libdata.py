import csv
import pandas as pd
from pymongo import MongoClient
import pymysql
from dataclasses import dataclass
from typing import Any


def load_hosts_csv(file_hosts_csv):
    """
    Load hosts.csv data from a file.

    Args:
        file_hosts_csv (str): The path to the hosts.csv file.

    Returns:
        dict: The loaded hosts.csv data.

    """
    dict_hosts = {}
    with open(file_hosts_csv, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        for row in spamreader:
            host_name, list_ip, list_os_info = eval(", ".join(row))
            dict_hosts[host_name] = {"ip": list_ip, "os": list_os_info} 
    return dict_hosts 

"""This class has methods for reading and writing data from/to CSV files, 
MySQL databases, and MongoDB databases. You can use it by creating an instance 
of DataLoader and calling the appropriate methods. Note that for MySQL and MongoDB, 
you need to provide a configuration dictionary when creating the DataLoader instance. 
This dictionary should contain the necessary information for connecting to the 
database (like host, user, password, etc.). 
"""


@dataclass
class DataLoader:
    """
    A class that provides methods to load and write data from/to different sources.
    """

    csv_path: str = None
    mysql_config: dict = None
    mongodb_config: dict = None

    def read_csv(self) -> pd.DataFrame:
        """
        Reads data from a CSV file and returns it as a pandas DataFrame.

        Returns:
            pd.DataFrame: The data read from the CSV file.
        """
        return pd.read_csv(self.csv_path)

    def write_csv(self, data: pd.DataFrame):
        """
        Writes the given data to a CSV file.

        Args:
            data (pd.DataFrame): The data to be written to the CSV file.
        """
        data.to_csv(self.csv_path, index=False)

    def read_mysql(self, query: str) -> pd.DataFrame:
        """
        Executes the given SQL query on a MySQL database and returns the result as a pandas DataFrame.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            pd.DataFrame: The result of the SQL query as a pandas DataFrame.
        """
        conn = pymysql.connect(**self.mysql_config)
        return pd.read_sql(query, conn)

    def write_mysql(self, data: pd.DataFrame, table_name: str):
        """
        Writes the given data to a MySQL database table.

        Args:
            data (pd.DataFrame): The data to be written to the MySQL database.
            table_name (str): The name of the table in the MySQL database.
        """
        conn = pymysql.connect(**self.mysql_config)
        data.to_sql(table_name, conn, if_exists='replace')

    def read_mongodb(self, collection_name: str) -> pd.DataFrame:
        """
        Reads data from a MongoDB collection and returns it as a pandas DataFrame.

        Args:
            collection_name (str): The name of the collection in the MongoDB database.

        Returns:
            pd.DataFrame: The data read from the MongoDB collection.
        """
        client = MongoClient(**self.mongodb_config)
        db = client.get_database()
        collection = db[collection_name]
        return pd.DataFrame(list(collection.find()))

    def write_mongodb(self, data: pd.DataFrame, collection_name: str):
        """
        Writes the given data to a MongoDB collection.

        Args:
            data (pd.DataFrame): The data to be written to the MongoDB collection.
            collection_name (str): The name of the collection in the MongoDB database.
        """
        client = MongoClient(**self.mongodb_config)
        db = client.get_database()
        collection = db[collection_name]
        data_dict = data.to_dict("records")
        collection.insert_many(data_dict)
        
    def csv_to_mysql(self, table_name: str):
        """
        Reads data from a CSV file and writes it to a MySQL database table.

        Args:
            table_name (str): The name of the table in the MySQL database.
        """
        data = self.read_csv()
        self.write_mysql(data, table_name)

    def mysql_to_csv(self):
        """
        Reads data from a MySQL database and writes it to a CSV file.
        """
        query = "SELECT * FROM table_name"
        data = self.read_mysql(query)
        self.write_csv(data)
    
    def csv_to_mongodb(self, collection_name: str):
        """
        Reads data from a CSV file and writes it to a MongoDB collection.

        Args:
            collection_name (str): The name of the collection in the MongoDB database.
        """
        data = self.read_csv()
        self.write_mongodb(data, collection_name)
        
    def mongodb_to_mysql(self, table_name: str):
        """
        Reads data from a MongoDB collection and writes it to a MySQL database table.

        Args:
            table_name (str): The name of the table in the MySQL database.
        """
        data = self.read_mongodb(collection_name)
        self.write_mysql(data, table_name)
        
    def mysql_to_mongodb(self, collection_name: str):
        """
        Reads data from a MySQL database and writes it to a MongoDB collection.

        Args:
            collection_name (str): The name of the collection in the MongoDB database.
        """
        query = "SELECT * FROM table_name"
        data = self.read_mysql(query)
        self.write_mongodb(data, collection_name)
        
    def create_mysql_table(mysql_config: dict, table_name: str, fields: dict):
        # Connect to the MySQL server
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()

        # Generate the SQL for creating the table
        fields_sql = ", ".join(f"{name} {type}" for name, type in fields.items())
        create_table_sql = f"CREATE TABLE {table_name} ({fields_sql})"

        # Execute the SQL
        cursor.execute(create_table_sql)

        # Close the connection
        conn.close()
        
    """mysql_config = {'host':'localhost', 'user':'username', 'password':'password', 'db':'database_name'}
fields = {'id': 'INT PRIMARY KEY', 'name': 'VARCHAR(100)', 'age': 'INT'}
create_mysql_table(mysql_config, 'table_name', fields)"""

    def create_mysql_database(mysql_config: dict, database_name: str):
        # Connect to the MySQL server
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()

        # Generate the SQL for creating the database
        create_database_sql = f"CREATE DATABASE {database_name}"

        # Execute the SQL
        cursor.execute(create_database_sql)

        # Close the connection
        conn.close()
        
    def drop_mysql_table(mysql_config: dict, table_name: str):
        # Connect to the MySQL server
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()

        # Generate the SQL for dropping the table
        drop_table_sql = f"DROP TABLE {table_name}"

        # Execute the SQL
        cursor.execute(drop_table_sql)

        # Close the connection
        conn.close()
        
    def drop_mysql_database(mysql_config: dict, database_name: str):
        # Connect to the MySQL server
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()

        # Generate the SQL for dropping the database
        drop_database_sql = f"DROP DATABASE {database_name}"

        # Execute the SQL
        cursor.execute(drop_database_sql)

        # Close the connection
        conn.close()
        
    def print_mysql_tables(mysql_config: dict):
        # Connect to the MySQL server
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()

        # Get the list of tables in the database
        cursor.execute("SHOW TABLES")

        # Print the list of tables
        for table in cursor.fetchall():
            print(table[0])

        # Close the connection
        conn.close()
        
    def print_mongodb_collections(mongodb_config: dict):
        # Connect to the MongoDB server
        client = MongoClient(**mongodb_config)
        db = client.get_database()

        # Get the list of collections in the database
        collections = db.list_collection_names()

        # Print the list of collections
        for collection in collections:
            print(collection)
            
        # Close the connection
        client.close()
        
    def print_csv_columns(csv_path: str):
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(csv_path)

        # Print the list of columns
        for column in data.columns:
            print(column)
            
    def print_mysql_columns(mysql_config: dict, table_name: str):
        # Connect to the MySQL server
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()

        # Get the list of columns in the table
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")

        # Print the list of columns
        for column in cursor.fetchall():
            print(column[0])

        # Close the connection
        conn.close()