import sqlite3
import functools
import logging
import sys

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
        # Get the query from the arguments (first positional argument in this case)
        query = args[0] if args else kwargs.get('query', 'Unknown query')
        # Log the query
        logging.info(f"Executing SQL query: {query}")
        # Call the original function with all arguments
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results



if __name__ == "__main__":
    try:
        users = fetch_all_users(query="SELECT * FROM users")
        print("Fetched users:", users)
    except sqlite3.Error as e:
        print(f"Database error: {e}")