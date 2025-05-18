import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "_dikachim@#!04770",
    "database": "ALX_prodev"
}

# Prototype: Generator to yield user ages one by one
def stream_user_ages():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch only the age column
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row[0]

    except mysql.connector.Error as err:
        print(f"Error streaming ages: {err}")
    finally:
        cursor.close()
        connection.close()

# Prototype: Calculate average age using the generator
def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    # Avoid division by zero
    if count == 0:
        return 0
    return total_age / count

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")