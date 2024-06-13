from flask import Flask, render_template, request, jsonify
import time
import traceback
import sys
import io

app = Flask(__name__)

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
        # Redirect stdout to capture print output
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        # Prepare a global context and stdin simulation
        global_context = {'sys': sys, 'input': io.StringIO(input_data).read}
        
        # Execute the function code in the global context
        exec(function_code, global_context)
        
        # Extract printed output
        result = new_stdout.getvalue().strip()
        
        # Reset stdout
        sys.stdout = old_stdout
    except Exception as e:
        # Reset stdout in case of an exception
        sys.stdout = old_stdout
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 400

    end_time = time.time()
    process_time = (end_time - start_time) * 1000  # in milliseconds
    return jsonify({'inputData': input_data, 'result': result, 'process_time': process_time})

if __name__ == '__main__':
    app.run(debug=True)


