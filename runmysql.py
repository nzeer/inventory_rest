from numpy import true_divide
import pymysql
from libdata import DataLoader as dl

# Define the MySQL database configuration
config = {
    'host': '172.16.30.30',
    'port': 3306,
    'user': 'root',
    'password': 'ANSKk08aPEDbFjDO',
    'db': 'inventory'
}

def main():
    # Connect to the MySQL server
    mysql_connection = dl()
    mysql_connection.set_mysql_config(config)

    # Define the SQL for creating the table
    create_table_sql = """
    CREATE TABLE example_table6 (
        id INT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
    """

    try:
        for t in mysql_connection.get_mysql_tables():
            for c in mysql_connection.get_mysql_columns(t):
                print("(\ntable: %s)[field: %s\n]" % (t, c))
    except Exception as e:
        print(e)

# Check if the script is run as the main module
if __name__ == "__main__":
    # Call the main function
    main()