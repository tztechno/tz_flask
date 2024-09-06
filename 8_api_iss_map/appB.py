from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/iss-data')
def iss_data():
    try:
        response = requests.get('https://api.wheretheiss.at/v1/satellites/25544')
        response.raise_for_status()  # HTTPエラーが発生した場合に例外をスロー
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
