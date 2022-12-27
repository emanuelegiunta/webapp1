import sqlite3
from flask import Flask, render_template
from settings import settings

def get_db_connection():
    connection = sqlite3.connect('database.db')
    # Apparently. the way in which rows are later accessed (in this case in a 
    # python dict-like way
    connection.row_factory = sqlite3.Row
    return connection

app = Flask(__name__)

@app.route(settings.path)
def index():
    connection = get_db_connection()
    # I'm not sure what fetchall does, but SELECT * FROM posts simply gets all
    #  entries from the table `posts`
    posts = connection.execute('SELECT * FROM posts').fetchall()
    return render_template('index_extended.html', posts=posts)

if __name__ == "__main__" and settings.path:
    app.run(debug=True)
