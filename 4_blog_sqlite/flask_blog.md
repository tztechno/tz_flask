FlaskとMongoDBを使用してシンプルなブログアプリケーションを作成しましょう。まずはFlaskとpymongoをインストールしましょう。。==> mongoは中止、sqliteを使うことに

```bash
pip install Flask pymongo
```

次に、プロジェクトを構築します。

1. **app.py**: Flaskアプリケーションを含みます。
2. **templates/**: レンダリング用のHTMLテンプレートを含みます。
3. **static/**: CSSやJavaScriptなどの静的ファイルを含みます。
4. **config.py**: 設定変数を含みます。
5. **models.py**: MongoDBのモデルを含みます。

以下に基本的な実装を示します。

**config.py:**
```python
class Config:
    SECRET_KEY = 'ここに秘密鍵を入力'
    MONGO_URI = 'mongodb://localhost:27017/blogdb'
```

**models.py:**
```python
from datetime import datetime
from flask_pymongo import PyMongo

mongo = PyMongo()

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.utcnow()

    @staticmethod
    def from_dict(data):
        return Post(data['title'], data['content'])
```

**app.py:**
```python
from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import mongo, Post

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

@app.route('/')
def index():
    posts = mongo.db.posts.find()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content)
        mongo.db.posts.insert_one(post.__dict__)
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>シンプルなブログ</title>
</head>
<body>
    <h1>シンプルなブログへようこそ</h1>
    <a href="{{ url_for('add') }}">新しい投稿を追加</a>
    <hr>
    {% for post in posts %}
    <div>
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
        <p>{{ post.created_at }}</p>
    </div>
    <hr>
    {% endfor %}
</body>
</html>
```

**templates/add.html:**
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>新しい投稿を追加</title>
</head>
<body>
    <h1>新しい投稿を追加</h1>
    <form action="{{ url_for('add') }}" method="POST">
        <label for="title">タイトル:</label><br>
        <input type="text" id="title" name="title"><br>
        <label for="content">コンテンツ:</label><br>
        <textarea id="content" name="content"></textarea><br>
        <button type="submit">送信</button>
    </form>
</body>
</html>
```

これで、新しい投稿を追加するシンプルなブログアプリケーションが完成しました。`app.py` を実行し、`http://localhost:5000` にアクセスしてブログを確認し、新しい投稿を追加できることを確認してください。

python app.py

http://127.0.0.1:5000

http://localhost:5000 にアクセスしてブログを確認し、新しい投稿を追加できることを確認してください。



---

記事の編集と削除機能を追加するには、いくつかの新しいルートとHTMLテンプレートが必要です。また、トップページ（`index.html`）で各記事に編集と削除のボタンを追加します。

以下は、Flaskアプリケーションに編集と削除の機能を追加するための手順です。

### 1. ルートを追加する

まず、Flaskアプリケーションに編集と削除のルートを追加します。

```python
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
```

### 2. HTMLテンプレートを追加・更新する

次に、HTMLテンプレートを更新して編集と削除の機能を追加します。

#### **index.html**

トップページで各記事に編集と削除のボタンを追加します。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Blog</title>
</head>
<body>
    <h1>Blog Posts</h1>
    <a href="{{ url_for('add') }}">Add New Post</a>
    <ul>
        {% for post in posts %}
            <li>
                <h2>{{ post[1] }}</h2>
                <p>{{ post[2] }}</p>
                <small>Posted on {{ post[3] }}</small><br>
                <a href="{{ url_for('edit', post_id=post[0]) }}">Edit</a>
                <form action="{{ url_for('delete', post_id=post[0]) }}" method="POST" style="display:inline;">
                    <button type="submit">Delete</button>
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
```

#### **add.html**

このファイルは変わりませんが、確認のために再掲します。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add New Post</title>
</head>
<body>
    <h1>Add a New Post</h1>
    <form action="{{ url_for('add') }}" method="POST">
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" required><br><br>
        <label for="content">Content:</label>
        <textarea id="content" name="content" rows="10" cols="30" required></textarea><br><br>
        <input type="submit" value="Add Post">
    </form>
    <a href="{{ url_for('index') }}">Back to Home</a>
</body>
</html>
```

#### **edit.html**

新しい編集用のテンプレートを作成します。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Post</title>
</head>
<body>
    <h1>Edit Post</h1>
    <form action="{{ url_for('edit', post_id=post[0]) }}" method="POST">
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" value="{{ post[1] }}" required><br><br>
        <label for="content">Content:</label>
        <textarea id="content" name="content" rows="10" cols="30" required>{{ post[2] }}</textarea><br><br>
        <input type="submit" value="Update Post">
    </form>
    <a href="{{ url_for('index') }}">Back to Home</a>
</body>
</html>
```

これで、記事の追加、編集、削除が可能な簡単なブログアプリケーションが完成します。各HTMLテンプレートは、`templates/`ディレクトリに保存してください。

### Flaskアプリケーションの実行

Flaskアプリケーションを実行するには、以下のコマンドを使用します。

```bash
python app.py
```

これにより、ローカルサーバーが起動し、ブラウザからブログアプリケーションにアクセスできるようになります。

http://127.0.0.1:5000
