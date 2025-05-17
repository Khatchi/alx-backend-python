#!/usr/bin/python3

import mysql.connector
# import time
from seed import connect_to_prodev

# # Implements Generator to stream rows one by one
# def stream_rows():
#     connection = connect_to_prodev()
#     if not connection:
#         return
#     try:
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM user_data")
#         for row in cursor:
#             yield row
#             time.sleep(0.1)
#     except mysql.connector.Error as err:
#         print(f"Error streaming rows: {err}")
#     finally:
#         cursor.close()
#         connection.close()


# Database configuration (same as in seed.py)
db_config = {
    "host": "localhost",
    "user": "root",  # Replace with your MySQL username
    "password": "_dikachim@#!04770",  # Replace with your MySQL password
    "database": "ALX_prodev"
}

# Prototype: Generator to stream rows one by one from user_data table
def stream_users():
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)  # Fetch rows as dictionaries

        # Fetch and yield rows one by one using a single loop
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:  # Single loop to stream rows
            yield row

    except mysql.connector.Error as err:
        print(f"Error streaming rows: {err}")
    finally:
        cursor.close()
        connection.close()