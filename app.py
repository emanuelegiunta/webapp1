import sqlite3
import os.path
from flask import Flask, render_template, request, url_for, flash, redirect
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

@app.route(os.path.join(settings.path, "create"), methods=('GET', 'POST'))
def create():
    if request.method == 'POST':

        # In the following we dangerously assume everything goes well, but it
        #  may also go wrong if the form is malformed
        title = request.form['title']
        content = request.form['content']

        if not title:
            # Not sure what flash does, but it seems like an `alert(<text>)`
            flash("title is required!")

        else:
            # Add to database
            connection = get_db_connection()
            connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))

            connection.commit()
            connection.close()
            return redirect(url_for('index'))

    # Se non siamo già tornati alla pagina iniziale, torniamo alla pagina
    return render_template('create.html')

@app.route(os.path.join(settings.path, "edit/<int:post_id>"),
    methods=('GET', 'POST'))
def edit(post_id):
    # This was the nice function we wrote with sqlite3
    post = get_post(post_id)

    if request.method == 'POST':

        # stuff form the form
        title = request.form['title']
        content = request.form['content']

        # Modify stuff in the database
        connection = get_db_connection()
        connection.execute("UPDATE posts SET title = ?, content = ?, created = CURRENT_TIMESTAMP WHERE id = ?", (title, content, post_id))

        connection.commit()
        connection.close()
        return redirect(url_for('index'))

    return render_template('edit.html', original_post=post)

@app.route(os.path.join(settings.path, "detele/<int:post_id>"),
    methods=('POST',))
def delete(post_id):

    # At some point I should work on a confirmation mechanism
    connection = get_db_connection()
    connection.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))

if __name__ == "__main__" and settings.path:
    app.run(debug=True)
