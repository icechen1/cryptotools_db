#a simple CRUD web service to handle public key storage and retrival for CryptoTools

from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#Some methods to be used internally
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
def get_entries():
    db = get_db()
    cur = db.execute('select nick, public_key from entries order by id desc')
    entries = cur.fetchall()
    return render_template('listing.html', entries=entries)
    
@app.route('/')
def home():
    #Returns the homepage and pass the urls to the template
    return render_template('index.htm')
    
@app.route('/result/<query>')
def result(query):
    # show the search results
    return get_entries()
    
@app.route('/result/')
def show_all_entries():
    # show the search results
    return get_entries()
    
@app.route('/add', methods=['POST'])
def add_entry():
    #if not session.get('logged_in'):
    #    abort(401)
    db = get_db()
    db.execute('insert into entries (nick, public_key) values (?, ?)',
                 [request.form['nick'], request.form['public_key']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_all_entries'))
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    #    return render_template('index.htm', error=error)
    
if __name__ == '__main__':
    app.run(debug=True)