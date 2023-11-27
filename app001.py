# app.py

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    # フォームからのデータを取得
    n_value = request.form.get('N')
    a_value = request.form.get('A')
    b_value = request.form.get('B')

    # データを表示
    return f'N: {n_value}, A: {a_value}, B: {b_value}'

if __name__ == '__main__':
    app.run(debug=True)
