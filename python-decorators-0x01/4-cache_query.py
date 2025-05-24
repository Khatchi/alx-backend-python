import time
import sqlite3
import functools
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Cache to store query results
query_cache = {}

def with_db_connection(func):
    """Decorator to handle opening and closing SQLite database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect('users.db')
            logging.info("Database connection opened.")
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                logging.info("Database connection closed.")
    return wrapper

def cache_query(func):
    """Decorator to cache database query results based on the query string."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from the arguments (assumes query is the first keyword argument)
        query = kwargs.get('query') if 'query' in kwargs else args[1] if len(args) > 1 else None
        if not query:
            logging.warning("No query found in arguments; executing without caching.")
            return func(*args, **kwargs)

        # Check if the query result is in the cache
        if query in query_cache:
            logging.info(f"Cache hit for query: {query}")
            return query_cache[query]

        # Cache miss: execute the query and store the result
        logging.info(f"Cache miss for query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        logging.info(f"Cached result for query: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    # First call will cache the result
    try:
        start_time = time.time()
        users = fetch_users_with_cache(query="SELECT * FROM users")
        print(f"First call (fetched from DB, time: {time.time() - start_time:.3f}s):", users)
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")

    # Second call will use the cached result
    try:
        start_time = time.time()
        users_again = fetch_users_with_cache(query="SELECT * FROM users")
        print(f"Second call (fetched from cache, time: {time.time() - start_time:.3f}s):", users_again)
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")