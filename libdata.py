import csv
import pandas as pd
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

config = {
    'host': '172.16.30.30',
    'port': 3306,
    'user': 'root',
    'password': 'p@s5w0rd',
    'db': 'testing'
}
"""


@dataclass
class DataLoader:
    def __init__(self, *, mysql_config: dict = {}, csv_path: str = ""):
        if mysql_config:
            self.set_mysql_config(mysql_config)
        
        if csv_path:
            self.set_csv_config_path(csv_path)
            
    def get_mysql_config(self) -> dict:
        return self.__dict__["_mysql_config"]
    
    def set_mysql_config(self, value: dict = {}):
        self.__dict__["_mysql_config"] = dict(value)
        
    def get_csv_config_path(self) -> str:
        return self.__dict__["_csv_config_path"]
    
    def set_csv_path(self, value: str = ""):
        self.__dict__["_csv_config_path"] = str(value)
        
    def read_csv(self) -> pd.DataFrame:
        """
        Reads data from a CSV file and returns it as a pandas DataFrame.

        Returns:
            pd.DataFrame: The data read from the CSV file.
        """
        data = None
        try:
            data = pd.read_csv(self.get_csv_config_path())
        except Exception as e:
            raise e
        
        return data

    def write_csv(self, data: pd.DataFrame) -> bool:
        """
        Writes the given data to a CSV file.

        Args:
            data (pd.DataFrame): The data to be written to the CSV file.
        """
        state = False
        try:
            data.to_csv(self.get_csv_config_path(), index=False)
            state = True
        except Exception as e:
            raise e
        finally:
            return state
    
    def csv_to_mysql(self, table_name: str) -> bool:
        """
        Reads data from a CSV file and writes it to a MySQL database table.

        Args:
            table_name (str): The name of the table in the MySQL database.
        """
        data = None
        state = False
        try:
            data = self.read_csv()
            self.write_mysql(data, table_name)
            state = True
        except Exception as e:
            raise e
        finally:
            return state
        
    def mysql_to_csv(self) -> bool:
        """
        Reads data from a MySQL database and writes it to a CSV file.
        """
        state = False
        query = "SELECT * FROM table_name"
        data = None
        try:
            data = self.read_mysql(query)
            self.write_csv(data)
            state = True
        except Exception as e:
            raise e
        finally:
            return state
        
    def print_csv_columns(self):
        """
        Prints the list of columns in the CSV file.
        """
        # Read the CSV file into a pandas DataFrame
        data = None
        if self.get_csv_path() is None:
            raise ValueError("CSV configuration is missing")
        try:
            data = pd.read_csv(self.get_csv_path())
            # Print the list of columns
            for column in data.columns:
                print(column)
        except Exception as e:
            raise e

    def read_mysql(self, query: str) -> pd.DataFrame:
        """
        Executes the given SQL query on a MySQL database and returns the result as a pandas DataFrame.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            pd.DataFrame: The result of the SQL query as a pandas DataFrame.
        """
        data = None
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                data = pd.read_sql(query, conn)
        except Exception as e:
            raise e
        return data

    def write_mysql(self, data: pd.DataFrame, table_name: str) -> bool:
        """
        Writes the given data to a MySQL database table.

        Args:
            data (pd.DataFrame): The data to be written to the MySQL database.
            table_name (str): The name of the table in the MySQL database.
        """
        state = False
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                data.to_sql(table_name, conn, if_exists='replace')
            state = True
        except Exception as e:
            raise e
        finally:
            return state

    def create_mysql_table(self, table_name: str, fields: dict) -> bool:
        """
        Creates a MySQL database table with the given table name and fields.

        Args:
            table_name (str): The name of the table in the MySQL database.
            fields (dict): The fields of the table with their data types.
        """
        state = False
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()
            
                # Generate the SQL for creating the table
                fields_sql = ", ".join(f"{name} {type}" for name, type in fields.items())
                create_table_sql = f"CREATE TABLE {table_name} ({fields_sql})"

                cursor.execute(create_table_sql)
            state = True
        except Exception as e:
            raise e
        finally:
            return state
        
    def create_mysql_database(self, database_name: str) -> bool:
        """
        Creates a MySQL database with the given name.

        Args:
            database_name (str): The name of the MySQL database to be created.
        """
        state = False
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()

                # Generate the SQL for creating the database
                create_database_sql = f"CREATE DATABASE {database_name}"

                cursor.execute(create_database_sql)
            state = True
        except Exception as e:
            raise e
        finally:
            return state
            
    def drop_mysql_table(self, table_name: str) -> bool:
        """
        Drops a MySQL database table with the given name.

        Args:
            table_name (str): The name of the table to be dropped.
        """
        state = False
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()

                # Generate the SQL for dropping the table
                drop_table_sql = f"DROP TABLE {table_name}"

                # Execute the SQL
                cursor.execute(drop_table_sql)
            state = True
        except Exception as e:
            raise e
        finally:
            return state
        
    def drop_mysql_database(self, database_name: str) -> bool:
        """
        Drops a MySQL database with the given name.

        Args:
            database_name (str): The name of the database to be dropped.
        """
        state = False
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()

                # Generate the SQL for dropping the database
                drop_database_sql = f"DROP DATABASE {database_name}"

                # Execute the SQL
                cursor.execute(drop_database_sql)
            state = True
        except Exception as e:
            raise e
        finally:
            return state
        
    def show_mysql_tables(self):
        """
        Prints the list of tables in the MySQL database.
        """
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()

                # Get the list of tables in the database
                cursor.execute("SHOW TABLES")
                # Print the list of tables
                for table in cursor.fetchall():
                    print(table[0])
        except Exception as e:
            raise e
        
    def get_mysql_tables(self) -> list:
        """
        Prints the list of tables in the MySQL database.
        """
        list_tables = []
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()

                # Get the list of tables in the database
                cursor.execute("SHOW TABLES")
                # Print the list of tables
                for table in cursor.fetchall():
                    list_tables.append(table[0])
        except Exception as e:
            raise e
        return list_tables
            
    def print_mysql_columns(self, table_name: str):
        """
        Prints the list of columns in the MySQL database table.

        Args:
            table_name (str): The name of the table in the MySQL database.
        """
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()
        
            
                # Get the list of columns in the table
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [column[0] for column in cursor.fetchall()]
            
                # Print the list of columns
                for column in columns:
                    print(column)

                # Get the list of columns in the table
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")

                # Print the list of columns
                for column in cursor.fetchall():
                    print(column[0])
        except Exception as e:
            raise e
        
    def get_mysql_columns(self, table_name: str) -> list:
        """
        Prints the list of columns in the MySQL database table.

        Args:
            table_name (str): The name of the table in the MySQL database.
        """
        list_columns = []
        # Connect to the MySQL server
        if self.get_mysql_config() is None:
            raise ValueError("MySQL configuration is missing")
        try:
            with pymysql.connect(**self.get_mysql_config()) as conn:
                cursor = conn.cursor()
        
            
                # Get the list of columns in the table
                #cursor.execute(f"DESCRIBE {table_name}")
                #columns = [column[0] for column in cursor.fetchall()]
            
                # Print the list of columns
                #for column in columns:
                #    print(column)

                # Get the list of columns in the table
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")

                # Print the list of columns
                for column in cursor.fetchall():
                    list_columns.append(column[0])
                #for column in cursor.fetchall():
                #    print(column[0])
                return list_columns
        except Exception as e:
            raise e

    def generate_mysql_insert_query(table_name: str, data: dict):
        """
        Generate the SQL query for inserting data into a MySQL table.

        Args:
            table_name (str): The name of the table.
            data (dict): A dictionary containing the column names as keys and the corresponding values.

        Returns:
            str: The SQL query for inserting the data into the table.
        """
        columns = ", ".join(data.keys())
        values = ", ".join(f"'{value}'" for value in data.values())
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        return insert_query
    
    def generate_mysql_update_query(table_name: str, data: dict, condition: str):
        """
        Generate the SQL query for updating data in a MySQL table.

        Args:
            table_name (str): The name of the table to update.
            data (dict): A dictionary containing the column-value pairs to update.
            condition (str): The condition to specify which rows to update.

        Returns:
            str: The generated SQL update query.
        """
        set_clause = ", ".join(f"{column} = '{value}'" for column, value in data.items())
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        return update_query
    
    def generate_mysql_delete_query(table_name: str, condition: str):
        """
        Generate the SQL query for deleting data from a MySQL table.

        Args:
            table_name (str): The name of the table from which data will be deleted.
            condition (str): The condition that specifies which rows to delete.

        Returns:
            str: The SQL query for deleting data from the table.
        """
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        return delete_query
    
    def generate_mysql_select_query(table_name: str, columns: list, condition: str = None):
        """
        Generate a MySQL SELECT query.

        Args:
            table_name (str): The name of the table to select from.
            columns (list): A list of column names to select.
            condition (str, optional): The condition to apply in the WHERE clause. Defaults to None.

        Returns:
            str: The generated SELECT query.
        """
        columns_str = ", ".join(columns)
        select_query = f"SELECT {columns_str} FROM {table_name}"
        if condition:
            select_query += f" WHERE {condition}"
        return select_query
    
    def execute_mysql_query(self, query: str) -> bool:
            """
            Executes a MySQL query.

            Args:
                query (str): The SQL query to be executed.

            Raises:
                ValueError: If MySQL configuration is missing.

            Returns:
                None
            """
            state = False
            # Connect to the MySQL server
            if self.get_mysql_config() is None:
                raise ValueError("MySQL configuration is missing")
            try:
                with pymysql.connect(**self.get_mysql_config()) as conn:
                    cursor = conn.cursor()

                    # Execute the SQL query
                    cursor.execute(query)

                    # Commit the changes
                    conn.commit()
                return True
                state = True
            except Exception as e:
                raise e
            
    def execute_mysql_insert_query(self, mysql_config: dict, table_name: str, data: dict) -> bool:
        """
        Executes a MySQL insert query to insert data into a specified table.

        Args:
            mysql_config (dict): A dictionary containing MySQL configuration parameters.
            table_name (str): The name of the table to insert the data into.
            data (dict): A dictionary containing the data to be inserted.

        Returns:
            None
        """
        state = False
        # Generate the SQL for inserting the data into the table
        insert_query = self.generate_mysql_insert_query(table_name, data)

        # Execute the SQL query
        try:
            if self.execute_mysql_query(mysql_config, insert_query):
                state = True
        except Exception as e:
            raise e
        finally:
            return state