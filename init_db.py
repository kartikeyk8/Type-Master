import sqlite3

# Define the name of the database file
DATABASE = 'typing_speed_test.db'

# Connect to the SQLite database
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create the 'results' table with the 'accuracy' column
cursor.execute('''
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    time_taken REAL NOT NULL,
    wpm REAL NOT NULL,
    accuracy REAL NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
