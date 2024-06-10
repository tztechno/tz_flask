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
