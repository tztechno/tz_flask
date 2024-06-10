
Sure, here's a simple Flask app that calculates Lucas numbers and sends the result and processing time back to the front-end using AJAX:

```python
from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

def lucas(n):
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        a, b = 2, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    start_time = time.time()
    data = request.json
    n = int(data['n'])
    result = lucas(n)
    end_time = time.time()
    process_time = (end_time - start_time) * 1000  # in milliseconds
    return jsonify({'result': result, 'process_time': process_time})

if __name__ == '__main__':
    app.run(debug=True)
```

Make sure you have the `index.html` file in the same directory as your `app.py` file. Also, ensure you have Flask installed (`pip install Flask`). This code defines a route `/calculate` that accepts POST requests, calculates the Lucas number for the given input, and returns the result along with the processing time in milliseconds.

python app.py

http://127.0.0.1:5000