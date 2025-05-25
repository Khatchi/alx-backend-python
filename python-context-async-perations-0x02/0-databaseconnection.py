#!/usr/bin/python3

import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class DatabaseConnection:
    """A context manager to handle SQLite database connections."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection and return it."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            logging.info(f"Opened database connection to {self.db_name}")
            return self.conn
        except sqlite3.Error as e:
            logging.error(f"Error opening database connection: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the database connection, handling any errors."""
        if self.conn:
            try:
                self.conn.close()
                logging.info(f"Closed database connection to {self.db_name}")
            except sqlite3.Error as e:
                logging.error(f"Error closing database connection: {e}")
                raise
        # If an exception occurred (exc_type is not None), it will be propagated
        # Do not suppress exceptions
        return False 

def setup_users_table(db_name):
    """Set up the users table in the database if it doesn't exist."""
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age int NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('INSERT INTO users (name, age, email) VALUES (?, ?, ?)', [
                ('solomon', 26, 'solomon@gmail.com'),
                ('mmesoma', 23, 'mmesoma@gmail.com'),
                ('kachi', 16, 'kachi@gmail.com'),
                ('oluchi', 24, 'oluchi@gmail.com'),
            ])
        conn.commit()
        logging.info("Users table created and populated with sample data (if not already present).")
    except sqlite3.Error as e:
        logging.error(f"Error setting up users table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Set up the database and table
    db_name = "users.db"
    setup_users_table(db_name)

    # Use the context manager to perform the query
    try:
        with DatabaseConnection(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            print("Query results:")
            for user in users:
                print(user)
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")