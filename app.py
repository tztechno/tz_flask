from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
    except sqlite3.Error as e:
        print(e)

def insert_post(conn, title, content):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO posts (title, content)
            VALUES (?, ?);
        ''', (title, content))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def get_posts(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM posts ORDER BY created_at DESC;
    ''')
    return cursor.fetchall()

def get_post(conn, post_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM posts WHERE id = ?;
    ''', (post_id,))
    return cursor.fetchone()

def update_post(conn, post_id, title, content):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE posts
            SET title = ?, content = ?
            WHERE id = ?;
        ''', (title, content, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def delete_post(conn, post_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM posts WHERE id = ?;
        ''', (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

@app.route('/')
def index():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        posts = get_posts(conn)
        conn.close()
        return render_template('index.html', posts=posts)
    return 'Database connection error.'

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = create_connection()
        if conn is not None:
            create_table(conn)
            insert_post(conn, title, content)
            conn.close()
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    conn = create_connection()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if conn is not None:
            update_post(conn, post_id, title, content)
            conn.close()
            return redirect(url_for('index'))
    else:
        post = get_post(conn, post_id)
        conn.close()
        if post:
            return render_template('edit.html', post=post)
    return 'Post not found.'

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    conn = create_connection()
    if conn is not None:
        delete_post(conn, post_id)
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
