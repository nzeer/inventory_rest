from libdata import DataLoader as dl

# Define the MySQL database configuration
MYSQLDB_CONFIG = {
    'host': '172.16.30.30',
    'port': 3306,
    'user': 'root',
    'password': 'ANSKk08aPEDbFjDO',
    'db': 'inventory'
}

def main():
    # Connect to the MySQL server
    mysql_connection = dl()
    mysql_connection.set_mysql_config(MYSQLDB_CONFIG)

    try:
        for t in mysql_connection.get_mysql_tables():
            print("Table: %s\n" % t.format())
            for c in mysql_connection.get_mysql_columns(t):
                print("\t[field: %s\n]" % (c.format()))
                #print("\n%s" % mysql_connection.get_mysql_data(t, c))
                print("\t\tField description: ", mysql_connection.get_mysql_field_description(t.format(), c.format()))
    except Exception as e:
        print(str(e))

# Check if the script is run as the main module
if __name__ == "__main__":
    # Call the main function
    main()