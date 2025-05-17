#!/usr/bin/python3

import mysql.connector
import time

# Configures the database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "_dikachim@#!04770"
}

# Connects to MYSQL server
def connect_db():
    try:
        connection = mysql.connector.connect(**db_config)
        print("Connected to MYSQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MYSQL server: {err}")
        return None
    
# Creates the ALX_prodev database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print(f"Database ALX_prodev created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

# Connects to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(database="ALX_prodev", **db_config)
        print("Connected to ALX_prodev.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None
    
# Creates the user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5, 2) NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """)
        print("Table user_data created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

# inserts data into user_data table if it doesn't exist
def insert_data(connection, data):
    try:
        cursor = connection.cursor()
        for row in data:
            # unpack the row
            user_id, name, email, age = row
            cursor.execute(
                "SELECT COUNT(*) FROM user_data WHERE user_id = %s", (user_id,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

# Implements Generator to stream rows one by one
def stream_rows():
    connection = connect_to_prodev()
    if not connection:
        return
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
            time.sleep(0.1)
    except mysql.connector.Error as err:
        print(f"Error streaming rows: {err}")
    finally:
        cursor.close()
        connection.close()