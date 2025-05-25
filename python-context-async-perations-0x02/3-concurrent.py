#!/usr/bin/python3

import asyncio
import aiosqlite
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# set up user table asynchronously using aiosqlite
async def setup_users_table(db_name):
    """Set up the users table with an age column in the database if it doesn't exist."""
    async with aiosqlite.connect(db_name) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Check if the table is empty
        cursor = await db.execute("SELECT COUNT(*) FROM users")
        count = (await cursor.fetchone())[0]
        if count == 0:
            await db.executemany('INSERT INTO users (name, age, email) VALUES (?, ?, ?)', [
                ('solomon', 26, 'solomon@gmail.com'),
                ('mmesoma', 23, 'mmesoma@gmail.com'),
                ('kachi', 41, 'kachi@gmail.com'),
                ('oluchi', 50, 'oluchi@gmail.com'),
            ])
        await db.commit()
        logging.info("Users table created and populated with sample data (if not already present).")

async def async_fetch_users():
    """Fetch all users from the database asynchronously."""
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        logging.info("Fetched all users.")
        return users

async def async_fetch_older_users():
    """Fetch users older than 40 from the database asynchronously."""
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        older_users = await cursor.fetchall()
        logging.info("Fetched users older than 40.")
        return older_users

async def fetch_concurrently():
    """Run the fetch operations concurrently using asyncio.gather."""
    # Set up the database and table
    await setup_users_table('users.db')

    # Run both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users

if __name__ == "__main__":
    # Run the concurrent fetch using asyncio.run
    all_users, older_users = asyncio.run(fetch_concurrently())

    # Print the results
    print("All users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)