import sqlite3

# This function takes the table name and a comma separated list of words to populate
def insert_words(table, words):
    """
    Insert a comma-separated list of words into a specified table.

    Args:
        table (str): The table name ("adjectives" or "animals").
        words (str): A comma-separated list of words to insert.
    """
    conn = sqlite3.connect("anonymous_references.db")
    cursor = conn.cursor()

    # Split the words by commas and strip any extra whitespace
    word_list = [word.strip() for word in words.split(",")]

    # Insert each word into the table
    for word in word_list:
        try:
            cursor.execute(f"INSERT INTO {table} (word) VALUES (?)", (word,))
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate: {word}")

    conn.commit()
    conn.close()
    print(f"Inserted words into {table} table successfully.")


insert_words("animals", "Armadillo, Auroch, Axolotl, Badger, Bat, Bear, Beaver, Buffalo, Camel, Capybara, Chameleon, Cheetah, Chinchilla, Chipmunk, Chupacabra, Cormorant, Coyote, Crow, Dingo, Dog, Dolphin, Duck, Eagle, Elephant, Falcon, Fox, Frog, Grizzly, Hawk, Hedgehog, Ibex, Ifrit, Jackal, Kangaroo, Koala, Kraken, Lemur, Leopard, Liger, Lion, Llama, Loris, Miner, Moon, Monkey, Moose, Orangutan, Otter, Owl, Panda, Penguin, Python, Rabbit, Raccoon, Raven, Squirrel, Tiger, Turtle, Vulture, Wolf, Wolverine, Teal")
