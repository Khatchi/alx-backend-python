#!/usr/bin/python3

import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

class ExecuteQuery:
    """A context manager to handle database connection and query execution."""
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open the connection, execute the query, and return the results."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.info(f"Executing query: {self.query} with params: {self.params}")
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            return self.results
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {e}")
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the cursor and connection, handle any errors."""
        if self.cursor:
            try:
                self.cursor.close()
            except sqlite3.Error as e:
                logging.error(f"Error closing cursor: {e}")
                raise
        if self.conn:
            try:
                self.conn.close()
                logging.info(f"Closed database connection to {self.db_name}")
            except sqlite3.Error as e:
                logging.error(f"Error closing database connection: {e}")
                raise
        # Do not suppress exceptions
        return False  


if __name__ == "__main__":
    #initializes db_name
    db_name = "users.db"

    # Use the context manager to execute the query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    try:
        with ExecuteQuery(db_name, query, params) as results:
            print("Query results (users with age > 25):")
            for user in results:
                print(user)
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")