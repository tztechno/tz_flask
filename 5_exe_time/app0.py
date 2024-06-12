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
