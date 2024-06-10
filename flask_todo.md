
Python Flaskを使用してToDoリストを作成するための単純な例を示します。このバージョンでは、データベースを使用せずに、ToDoアイテムをリストとして保持します。

まず、`Flask` をインストールしましょう。

```bash
pip install Flask
```

次に、ToDoアプリを作成します。以下が `app.py` のコードです。

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ToDoリストを保持するためのリスト
todo_list = []

@app.route('/')
def index():
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    item = request.form['item']
    todo_list.append(item)
    return redirect(url_for('index'))

@app.route('/remove/<int:index>')
def remove(index):
    if 0 <= index < len(todo_list):
        del todo_list[index]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

次に、ToDoアプリ用のHTMLテンプレート `index.html` を作成します。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ToDo App</title>
</head>
<body>
    <h1>ToDo List</h1>
    <ul>
        {% for item in todo_list %}
        <li>
            {{ item }}
            <a href="/remove/{{ loop.index0 }}">[x]</a>
        </li>
        {% endfor %}
    </ul>
    <form action="/add" method="post">
        <input type="text" name="item" placeholder="ToDoを追加">
        <button type="submit">追加</button>
    </form>
</body>
</html>
```

これで、ToDoアプリが完成しました。ToDoを追加するには、フォームにテキストを入力して「追加」ボタンをクリックします。ToDoを完了するには、ToDoの横にある `[x]` リンクをクリックします。

これで、ToDoアプリのベースができました。必要に応じて、デザインや機能を追加できます。

python app.py

http://127.0.0.1:5000