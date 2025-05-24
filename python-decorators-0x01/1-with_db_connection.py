import sqlite3
import functools
import logging
from datetime import datetime

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def with_db_connection(func):
    """Decorator to handle opening and closing SQLite database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Open the database connection
            conn = sqlite3.connect('users.db')
            logging.info("Database connection opened.")
            
            # Call the function, passing the connection as the first argument
            result = func(conn, *args, **kwargs)
            return result
            
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            # Re-raise the exception for the caller to handle
            raise
        finally:
            # Close the connection if it was opened
            if conn:
                conn.close()
                logging.info("Database connection closed.")
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":

    # Fetch user by ID with automatic connection handling
    try:
        user = get_user_by_id(user_id=1)
        print("User:", user)
    except sqlite3.Error as e:
        print(f"Error fetching user: {e}")