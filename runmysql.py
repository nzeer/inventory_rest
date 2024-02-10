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
        #if mysql_connection.execute_mysql_query(create_table_sql):
        #    print("Table created successfully")
        pass
    except Exception as e:
        print(e)

    #mysql_connection.show_mysql_tables()

    for t in mysql_connection.get_mysql_tables():
        for c in mysql_connection.get_mysql_columns(t):
            print("(\ntable: %s)[field: %s\n]" % (t, c))
        
        #print(mysql_connection.print_mysql_columns(t))
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

# Check if the script is run as the main module
if __name__ == "__main__":
    # Call the main function
    main()