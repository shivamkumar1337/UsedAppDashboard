import psycopg2
from psycopg2 import Error

# Function to connect to PostgreSQL database
def connect_to_postgres():
    try:
        # Connect to an existing database
        connection = psycopg2.connect(
            user="postgres",
            password="12345",
            host="localhost",
            port="5433",
            database="AppUsageDatabase",
            # client_encoding='utf8'
        )

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        return connection, cursor

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None, None


# Function to insert data into the table
def insert_data(connection, cursor):
    try:
        # Example data to be inserted
        # app_name = "MyApp"
        # start_time = datetime(2024, 6, 27, 10, 0, 0)  # Replace with actual start time
        # end_time = datetime(2024, 6, 27, 11, 0, 0)    # Replace with actual end time
        # duration = end_time - start_time
        name = 123
        data = "shivam"
        # Insert data query
        insert_query = '''
            INSERT INTO stu (name, data)
            VALUES (%s, %s)
        '''

        # Data to be inserted
        record_to_insert = (name, data)

        # Execute the INSERT statement
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        print("Data inserted successfully")

    except (Exception, Error) as error:
        print("Error while inserting data into PostgreSQL", error)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


# Main function
if __name__ == "__main__":
    # Connect to PostgreSQL
    connection, cursor = connect_to_postgres()

    if connection and cursor:
        # Add data to PostgreSQL
        insert_data(connection, cursor)
