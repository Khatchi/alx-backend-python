import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ALX_prodev"
}

# Prototype: Fetch a specific page of users with given page_size and offset
def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Fetch the page using LIMIT and OFFSET
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        page = cursor.fetchall()
        return page

    except mysql.connector.Error as err:
        print(f"Error fetching page: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

# Prototype: Generator to lazily paginate through user_data table
def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size