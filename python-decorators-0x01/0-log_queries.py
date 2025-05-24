import sqlite3
import functools
import logging
import sys
from datetime import datetime

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from the arguments 
        query = args[0] if args else kwargs.get('query', 'Unknown query')
        # Log the query
        logging.info(f"Executing SQL query: {query}")
        # Call the original function with all arguments
        result = func(*args, **kwargs)
        return result
    return wrapper

# Set up the users table if it doesn't exist
def setup_users_table():
    """Set up the users table in users.db if it doesn't exist."""
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', [
                ('solomon', 'solomon@gmail.com'),
                ('kachi', 'kachi@gmail.com'),
                ('dikachim', 'dikachim@gmail.com'),
            ])
        conn.commit()
        logging.info("Users table created and populated with sample data (if not already present).")
    except sqlite3.Error as e:
        logging.error(f"Error setting up users table: {e}")
    finally:
        conn.close()

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results



if __name__ == "__main__":
    
    setup_users_table()
    try:
        users = fetch_all_users(query="SELECT * FROM users")
        print("Fetched users:", users)
    except sqlite3.Error as e:
        print(f"Database error: {e}")