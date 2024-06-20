from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    db_path = 'sqlite-sakila.db'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # テーブル名を取得
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(query)
    tables = cursor.fetchall()
    
    if not tables:
        return "No tables found in the database."

    table = tables[0]
    
    # テーブルのデータを取得
    query = f"SELECT * FROM {table[0]};"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # 最初の3行を表示
    display_rows = rows[:6]
    
    # カラム名を取得
    column_names = [description[0] for description in cursor.description]

    connection.close()
    
    return render_template('index.html', rows=display_rows, columns=column_names)

if __name__ == '__main__':
    app.run(debug=True)
