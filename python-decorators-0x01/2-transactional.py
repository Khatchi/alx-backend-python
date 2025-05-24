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

def transactional(func):
    """Decorator to manage database transactions with commit/rollback."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Ensure the connection is in a transaction
        original_isolation = conn.isolation_level
        # Switch to manual transaction control
        conn.isolation_level = None 
        cursor = conn.cursor()
        try:
            # Begin the transaction
            cursor.execute("BEGIN TRANSACTION")
            logging.info("Transaction started.")

            # Execute the function
            result = func(conn, *args, **kwargs)

            # Commit the transaction
            conn.commit()
            logging.info("Transaction committed.")
            return result

        except Exception as e:
            # Roll back the transaction on any error
            conn.rollback()
            logging.error(f"Transaction rolled back due to error: {e}")
            # Re-raise the exception for the caller to handle
            raise  

        finally:
            # Restore the original isolation level
            conn.isolation_level = original_isolation
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Function to fetch a user for verification
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    # Fetch user before update
    try:
        user_before = get_user_by_id(user_id=1)
        print("User before update:", user_before)
    except sqlite3.Error as e:
        print(f"Error fetching user: {e}")

    # Update user's email with automatic transaction handling
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        print("Email updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating email: {e}")

    # Fetch user after update to verify
    try:
        user_after = get_user_by_id(user_id=1)
        print("User after update:", user_after)
    except sqlite3.Error as e:
        print(f"Error fetching user: {e}")