
# ユーザーが定義した関数と入力値を入力し、計算結果と計算時間を得る

python app.py

http://127.0.0.1:5000

---

再帰関数の例で成功したのは良いニュースです。どこを変更したかについて詳細に説明します。

以下に成功した可能性が高い修正点をまとめます。

### 修正点

1. **グローバルコンテキストの設定**:
   - `exec`関数の実行に使うグローバルコンテキストを設定しました。これにより、ユーザーが入力した`lucas`関数がグローバルスコープで認識されるようになります。

2. **エラーハンドリングの強化**:
   - エラーが発生した場合、エラーメッセージとスタックトレースをクライアントに返すようにしました。これにより、どの部分で問題が発生しているのかを容易に特定できます。

3. **関数の抽出**:
   - `exec`関数でユーザーのコードを実行した後、`lucas`関数を正しく抽出しました。

以下が最終的なコードです。

#### `app.py`

```python
from flask import Flask, render_template, request, jsonify
import time
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start_time = time.time()
    data = request.json
    n = int(data['n'])
    function_code = data['functionCode']
    
    try:
        # Define a global context dictionary
        global_context = {}
        
        # Execute the function code in the global context
        exec(function_code, global_context)
        
        # Extract the lucas function
        lucas = global_context['lucas']
        
        # Calculate the result using the lucas function
        result = lucas(n)
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 400

    end_time = time.time()
    process_time = (end_time - start_time) * 1000  # in milliseconds
    return jsonify({'result': result, 'process_time': process_time})

if __name__ == '__main__':
    app.run(debug=True)
```

### 成功の要因

1. **グローバルコンテキストの設定**:
   - `exec(function_code, global_context)`を使用して、ユーザーが入力した関数がグローバルスコープで実行されるようにしました。これにより、再帰的な呼び出しが正しく機能します。

2. **関数の抽出**:
   - `global_context`から`lucas`関数を抽出することで、正しく呼び出せるようにしました。

3. **エラーハンドリング**:
   - エラーメッセージとスタックトレースをフロントエンドに返すことで、問題の特定が容易になりました。

これらの修正点により、ユーザーが定義した再帰関数を正しく実行できるようになったと考えられます。再度テストを行い、問題がないか確認してみてください。

python app.py

http://127.0.0.1:5000


----

関数の名前を一定で定義する必要はありません。ユーザーが任意の関数名を使えるようにする方法もあります。そのためには、フロントエンドでユーザーに関数名を入力させ、バックエンドでその関数名を使って動的に関数を呼び出す必要があります。

以下はその実装例です。

### フロントエンド（index.html）

ユーザーが関数名を指定できるように、関数名を入力するフィールドを追加します。

```html
<!DOCTYPE html>
<html>
<head>
    <title>Function Execution Time Calculator</title>
</head>
<body>
    <h1>Function Execution Time Calculator</h1>
    <p>Define your function:</p>
    <textarea id="functionCode" rows="10" cols="50">def my_function(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return my_function(n-2) + my_function(n-1)</textarea>
    <p>Enter the function name:</p>
    <input type="text" id="functionName" placeholder="Enter the function name">
    <p>Enter a number to calculate:</p>
    <input type="number" id="inputN" placeholder="Enter a number">
    <button onclick="sendRequest()">Calculate</button>
    <div id="result"></div>
    <div id="time"></div>
    <div id="error" style="color: red;"></div>

    <script>
        function sendRequest() {
            const n = document.getElementById('inputN').value;
            const functionCode = document.getElementById('functionCode').value;
            const functionName = document.getElementById('functionName').value;
            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ n, functionCode, functionName })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('error').innerText = `Error: ${data.error}`;
                    } else {
                        document.getElementById('result').innerText = `Result = ${data.result}`;
                        document.getElementById('time').innerText = `Time: ${(data.process_time / 1000).toFixed(3)} sec`;
                        document.getElementById('error').innerText = '';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('error').innerText = `Error: ${error}`;
                });
        }
    </script>
</body>
</html>
```

### バックエンド（app.py）

関数名を動的に指定できるように修正します。

```python
from flask import Flask, render_template, request, jsonify
import time
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start_time = time.time()
    data = request.json
    n = int(data['n'])
    function_code = data['functionCode']
    function_name = data['functionName']
    
    try:
        # Define a global context dictionary
        global_context = {}
        
        # Execute the function code in the global context
        exec(function_code, global_context)
        
        # Extract the function by name
        if function_name not in global_context:
            raise ValueError(f"Function {function_name} is not defined.")
        
        user_function = global_context[function_name]
        
        # Calculate the result using the user-defined function
        result = user_function(n)
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 400

    end_time = time.time()
    process_time = (end_time - start_time) * 1000  # in milliseconds
    return jsonify({'result': result, 'process_time': process_time})

if __name__ == '__main__':
    app.run(debug=True)
```

### 説明

- **フロントエンド** (`index.html`):
  - ユーザーに関数コードと関数名を入力させるフィールドを追加しました。
  - 入力された関数名をバックエンドに送信します。

- **バックエンド** (`app.py`):
  - `exec`で関数コードを実行し、ユーザーが指定した関数名を使ってグローバルコンテキストから関数を抽出します。
  - 指定された関数が存在しない場合はエラーを返します。
  - 関数が存在する場合はその関数を使って計算を行います。

これにより、ユーザーは任意の関数名と関数コードを指定して実行できるようになります。これが求める柔軟なソリューションです。

---


それは良かったです！お役に立てて嬉しいです。このアプリケーションは、ユーザーが任意の関数を定義し、その実行結果と計算時間を確認できる非常に柔軟なツールになりました。

まとめ
フロントエンド: ユーザーが関数コードと関数名を入力し、計算結果と処理時間を表示。
バックエンド: ユーザーが入力した関数を動的に実行し、結果と計算時間をJSON形式で返す。
アプリケーションの利点
柔軟性: 任意の関数を定義して実行できるため、多様な用途に対応可能。
使いやすさ: シンプルなインターフェースで関数を入力し、即座に結果を確認できる。
拡張性: 他の機能を追加して、さらなるカスタマイズや機能強化が可能。
次のステップ
もしさらにアプリケーションを拡張したい場合、以下のようなアイディアがあります：

複数の入力: 複数の引数を受け取る関数に対応する。
関数ライブラリ: よく使う関数を保存し、再利用できるようにする。
グラフィカルな結果表示: 結果をグラフなどで視覚的に表示する。
ユーザー認証: 複数のユーザーがそれぞれの関数を管理できるようにする。
コードの管理
バージョン管理: Gitなどのバージョン管理システムを使ってコードの変更履歴を管理する。
ドキュメント: コードの使い方や機能をまとめたドキュメントを作成し、将来的なメンテナンスや拡張を容易にする。
また、何か質問があれば、いつでもお知らせください。今後のプロジェクトが成功することを願っています！

---

python app.py

http://127.0.0.1:5000