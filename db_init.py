import sqlite3

# Create a new SQLite database
conn = sqlite3.connect("anonymous_references.db")
cursor = conn.cursor()

# Create tables for adjectives, animals and references
cursor.execute("CREATE TABLE IF NOT EXISTS adjectives (id INTEGER PRIMARY KEY, word TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS animals (id INTEGER PRIMARY KEY, word TEXT)")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS name_references (
        id INTEGER PRIMARY KEY,
        random_name TEXT UNIQUE,
        link_or_string TEXT
    )
""")

conn.commit()
conn.close()