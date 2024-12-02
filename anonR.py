import sqlite3
import argparse
import pyperclip

# Configurable database name used in setup
DATABASE_NAME = "anonymous_references.db"

def get_connection():
    """Returns a connection to the configured database."""
    return sqlite3.connect(DATABASE_NAME)

# Create or connect to the database and ensure the table exists
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS name_references (
            random_name TEXT UNIQUE,
            link_or_string TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adjectives (word TEXT UNIQUE)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animals (word TEXT UNIQUE)
    """)
    conn.commit()
    conn.close()

# Get a random word from the specified table
def get_random_word(table):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT word FROM {table} ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Generate a random name
def generate_anonymous_name():
    adjective = get_random_word("adjectives")
    animal = get_random_word("animals")
    return f"{adjective} {animal}"

# Save the link or string with the generated random name
def save_reference(link_or_string):
    random_name = generate_anonymous_name()
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        try:
            cursor.execute("""
                INSERT INTO name_references (random_name, link_or_string)
                VALUES (?, ?)
            """, (random_name, link_or_string))
            conn.commit()
            break
        except sqlite3.IntegrityError:
            # Handle duplicate names
            random_name = generate_anonymous_name()

    conn.close()
    return random_name

# Retrieve the link or string using the random name
def get_reference(random_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT link_or_string FROM name_references WHERE LOWER(random_name) = ?
    """, (random_name.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# List all references
def list_references():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT random_name, link_or_string FROM name_references")
    results = cursor.fetchall()
    conn.close()
    return results

# Delete a reference
def delete_reference(random_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM name_references WHERE LOWER(random_name) = ?
    """, (random_name.lower(),))
    conn.commit()
    conn.close()

# Create a new reference with a specific name and link
def create_reference(random_name, link_or_string):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO name_references (random_name, link_or_string)
            VALUES (?, ?)
        """, (random_name, link_or_string))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Error: The name '{random_name}' already exists.")
    conn.close()

# Main CLI functionality
def main():
    setup_database()

    parser = argparse.ArgumentParser(description="Anonymous References")
    parser.add_argument("--save", metavar="LINK", help="Save a new reference with a random name")
    parser.add_argument("--retrieve", metavar="NAME", help="Retrieve a reference by its name")
    parser.add_argument("--list", action="store_true", help="List all references")
    parser.add_argument("--delete", metavar="NAME", help="Delete a reference by its name")
    parser.add_argument("--create", nargs=2, metavar=("NAME", "LINK"), help="Create a reference with a specific name and link")

    args = parser.parse_args()

    if args.save:
        random_name = save_reference(args.save)
        print(f"Saved! Name: {random_name}")
    elif args.retrieve:
        reference = get_reference(args.retrieve)
        if reference:
            print(f"Retrieved: {reference}")
            pyperclip.copy(reference)
            print("Copied to clipboard!")
        else:
            print("Reference not found.")
    elif args.list:
        references = list_references()
        if references:
            print("All references:")
            for name, link in references:
                print(f"{name}: {link}")
        else:
            print("No references found.")
    elif args.delete:
        delete_reference(args.delete)
        print(f"Deleted reference: {args.delete}")
    elif args.create:
        name, link = args.create
        create_reference(name, link)
        print(f"Created reference: {name} -> {link}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
