from numpy import true_divide
import pymysql
from libdata import DataLoader as dl

# Define the MySQL database configuration
config = {
    'host': '172.16.30.30',
    'port': 3306,
    'user': 'root',
    'password': 'ANSKk08aPEDbFjDO',
    'db': 'testing'
}
#data_loader = DataLoader()
#print(config)
mysql_connection = dl()
dl.mysql_config = config
# Connect to the MySQL server
#conn = pymysql.connect(**config)
#cursor = conn.cursor()

# Define the SQL for creating the table
create_table_sql = """
CREATE TABLE example_table6 (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT
)
"""

try:
    if mysql_connection.execute_mysql_query(create_table_sql):
        print("Table created successfully")
except Exception as e:
    print(e)

mysql_connection.show_mysql_tables()
# Execute the SQL to create the table
#cursor.execute(create_table_sql)

# Define the SQL for listing all tables in the database
#show_tables_sql = "SHOW TABLES"

# Execute the SQL to list all tables
#cursor.execute(show_tables_sql)

# Fetch and print all tables
#tables = cursor.fetchall()
#for table in tables:
#    print(table)

# Close the connection
#conn.close()