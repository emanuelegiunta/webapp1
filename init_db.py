import sqlite3

connection = sqlite3.connect("database.db")

# We execute a query from file
with open('./schema.sql') as f:
    connection.executescript(f.read())

# I'm not experienced with SQLite, but the `connection` and `cursor` objects
# seem to be the main one to work with (TODO, read their docs)

cur = connection.cursor()

# We execute a query directly form here
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
            ('First Post', 'Content for the first post'))

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post'))

connection.commit()
connection.close()