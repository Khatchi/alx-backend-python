import time
import sqlite3
import functools
import logging

# Configure logging
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

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function on failure with a specified number of retries and delay."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            last_exception = None

            while attempt <= retries + 1:  # Include the initial attempt
                try:
                    logging.info(f"Attempt {attempt} to execute {func.__name__}.")
                    result = func(*args, **kwargs)
                    logging.info(f"Successfully executed {func.__name__} on attempt {attempt}.")
                    return result

                except sqlite3.Error as e:
                    last_exception = e
                    # Last attempt failed
                    if attempt == retries + 1:
                        logging.error(f"Failed to execute {func.__name__} after {retries + 1} attempts: {e}")
                        # Re-raise the last exception
                        raise  

                    logging.warning(f"Attempt {attempt} failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    attempt += 1

            # This line should never be reached due to the raise above, but included for clarity
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

if __name__ == "__main__":
    # Attempt to fetch users with automatic retry on failure
    try:
        users = fetch_users_with_retry()
        print("Fetched users:", users)
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")