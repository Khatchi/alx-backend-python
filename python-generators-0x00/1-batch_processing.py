#!/usr/bin/python3
import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",  
    "password": "_dikachim@#!04770",  
    "database": "ALX_prodev"
}

# Prototype: Generator to fetch rows in batches from user_data table
def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Fetch all rows (MySQL Connector doesn't support native batch fetching with LIMIT/OFFSET in a generator-friendly way)
        cursor.execute("SELECT * FROM user_data")
        batch = []
        for row in cursor:  # Loop 1: Fetch rows and build batches
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:  # Yield the last batch if it's not empty
            yield batch

    except mysql.connector.Error as err:
        print(f"Error streaming batches: {err}")
    finally:
        cursor.close()
        connection.close()

# Prototype: Process batches to filter users over age 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size): 
        # Filter users over age 25 in the batch
        filtered_batch = [user for user in batch if user['age'] > 25]
        if filtered_batch:
            yield filtered_batch
    
    return