

AtCoderのコードテストページでは、言語を選んで、標準入力とソースコードをテキストBOXから入力して実行することで、標準出力と実行時間がわかります。
今回は、Python言語において、コードテストページに相当する働きをするWebアプリをflaskで作成し、Vercelにデプロイしました。
このアプリでは、AtCoder問題の入力例や解答に提出するソースコードをそのまま入力に使うことが出来て、実行することで出力結果、計算時間を知ることが出来ます。
ただし、出力結果の正誤判定はできません。計算時間は9秒間がMAXで、それを超えると'処理が9秒を超えたため強制終了しましたの'メッセージが表示されます


## ファイル階層
```text
myapp/
├── templates/
│   └── index.html
├── index.py
├── requirements.txt
└── vercel.json
```

##　index.py
```
from flask import Flask, render_template, request, jsonify
import time
import traceback
import sys
import io
import signal

app = Flask(__name__)

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("処理が9秒を超えました")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start_time = time.time()
    data = request.json
    input_data = data['inputData']
    function_code = data['functionCode']
    
    try:
        # 9秒のタイマーを設定
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(9)
        
        # Redirect stdout to capture print output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Simulate stdin
        stdin = io.StringIO(input_data)
        global_context = {'sys': sys, 'input': stdin.readline}
        
        # Execute the function code in the global context
        exec(function_code, global_context)
        
        # Get the captured output
        result = captured_output.getvalue().strip()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # タイマーをリセット
        signal.alarm(0)
    except TimeoutException as e:
        # Reset stdout in case of a timeout
        sys.stdout = sys.__stdout__
        return jsonify({'error': str(e), 'result': '処理が9秒を超えたため強制終了しました', 'process_time': 9000}), 200
    except Exception as e:
        # Reset stdout in case of an exception
        sys.stdout = sys.__stdout__
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 400

    end_time = time.time()
    process_time = (end_time - start_time) * 1000  # in milliseconds
    return jsonify({'inputData': input_data, 'result': result, 'process_time': process_time})

if __name__ == '__main__':
    app.run()
```

##　index.html
```
<!DOCTYPE html>
<html>

<head>
    <title>Python Run Time Calculator</title>
</head>

<body>
    <h1>Python Run Time Calculator</h1>
    <p>Define your function:</p>
    <textarea id="functionCode" rows="10" cols="50">
n = int(input())
print(n*n)
    </textarea>
    <p>Enter your input (multiple lines allowed):</p>
    <textarea id="inputData" rows="5" cols="50" placeholder="Enter input data"></textarea>
    <button onclick="sendRequest()">Calculate</button><br><br>
    <div id="inputDisplay"></div>
    <div id="result"></div>
    <div id="time"></div>
    <div id="error" style="color: red;"></div>

    <script>
        function sendRequest() {
            const inputData = document.getElementById('inputData').value;
            const functionCode = document.getElementById('functionCode').value;
            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ inputData, functionCode })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('error').innerText = `Error: ${data.error}`;
                    } else {
                        document.getElementById('inputDisplay').innerText = `Input:\n${data.inputData}`;
                        document.getElementById('result').innerText = `Result:\n${data.result}`;
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
```



```
```
```

```
```
```
```
```
```
```
```
