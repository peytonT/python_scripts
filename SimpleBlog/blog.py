from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

#config
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'

# os.urandom(24)
SECRET_KEY = "\xd96\x92\xf29\x1al\xdc_\x83\x86\xb8@\x06\xd3\xa2\xbefN\x9a\xd3\x9b\xf4"


app = Flask(__name__)

# get app config by looking for UPPERCASE vars
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# GET is used by default
# POST when logging in
# GET after logging out: redirect to the login page
@app.route('/', methods = ['GET', 'POST'])
def login():
    err = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            err = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=err)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')  # message in get_flash_message
    return redirect(url_for('login'))

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']

    if not title or not post:
        flash('All fields required. Please try again.')
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('insert into posts (title, post) values (?,?)',
            [request.form['title'], request.form['post']])
        g.db.commit()
        g.db.close()
        flash('New entry posted!')
        return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
