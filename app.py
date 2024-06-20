from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLiteデータベースファイルのパス
sqlite_db_path = '/Users/shun_ishii/Projects/pj1/myapp/database.sqlite'

# ホームページ
@app.route('/')
def home():
    return render_template('index.html')

# SQL実行エンドポイント
@app.route('/execute-sql', methods=['POST'])
def execute_sql():
    try:
        # テキストボックスからのSQL文を取得
        sql_statement = request.form['sql']

        # SQLiteデータベースに接続
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()

        # SQL文を実行
        cursor.execute(sql_statement)

        # SELECT文の場合は結果を取得
        if sql_statement.strip().upper().startswith('SELECT'):
            columns = [col[0] for col in cursor.description]
            results = cursor.fetchall()
            response = {'columns': columns, 'data': results}
        else:
            conn.commit()
            response = {'message': 'SQL statement executed successfully.'}

        # データベースとの接続を閉じる
        conn.close()

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
