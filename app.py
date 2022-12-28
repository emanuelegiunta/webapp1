import sqlite3
import os.path
from flask import Flask, render_template
from werkzeug.exceptions import abort
from settings import settings

def get_db_connection():
    '''Opens the database and return a `connection` object (entries of a table
    can be iterated over this object. Rows will behave as dictionaries)
    '''

    connection = sqlite3.connect('database.db')
    # Apparently. the way in which rows are later accessed (in this case in a 
    # python dict-like way
    connection.row_factory = sqlite3.Row
    return connection

def get_post(post_id):
    '''Get a post given a post ID, or else raises a NotFound error
    '''

    # For some reason we can't reuse the connection as we did before
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    post = connection.execute('SELECT * FROM posts WHERE id = ?', 
                              (post_id,)).fetchone()
    connection.close()

    # Apparently post is either None or a string if the entry is non-empty
    #  Thus we only 'match' against None and not-None
    if post is None:
        # Raise an Error 404
        abort(404)

    return post


#==============================================================================
# FLASK STUFF

app = Flask(__name__)

# Inject variables into Jinja Template Processor
@app.context_processor
def inject_settings():
    return {'settings': settings}

# by default settings.path = "/" so the line below is read as
# `@app.route("/")`
@app.route(settings.path)
def index():
    connection = get_db_connection()
    # I'm not sure what fetchall does, but SELECT * FROM posts simply gets all
    #  entries from the table `posts`
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index_extended.html', posts=posts)

# Create a family of sub-pages. Each pages is associated to an int `post_id`
#  ie. `/test/1` `/test/2` if `settings.path` is "/test/"
@app.route(os.path.join(settings.path, "<int:post_id>"))
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

if __name__ == "__main__" and settings.path:
    app.run(debug=True)
