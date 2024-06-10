Flaskアプリケーションを作成して、このスクレイピングコードを使ってデータを取得し、フロントエンドに表示することができます。以下はその例です。

まず、必要なライブラリをインストールします。

```bash
pip install flask beautifulsoup4 requests pandas
```

次に、以下のようなディレクトリ構造でファイルを配置します。

```
project/
│
├── app.py
└── templates/
    └── index.html
```

`app.py` ファイルには次のようなコードを記述します。

```python
from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import urllib.request
import pandas as pd

app = Flask(__name__)

def scrape_data():
    url = 'https://www.fda.gov/drugs/guidances-drugs/newly-added-guidance-documents'
    source = urllib.request.urlopen(url)
    soup = BeautifulSoup(source, 'lxml')
    
    tags = soup.find('table', class_="table table-striped")
    
    table_data = []
    for row in tags.find_all('tr'):
        row_data = [cell.text for cell in row.find_all(['th', 'td'])]
        table_data.append(row_data)
    
    n = 8
    df = pd.DataFrame(columns=table_data[0], index=range(n))
    
    for i in range(n):
        table_data[i][0] = table_data[i][0].replace('\n', '')
        table_data[i][1] = table_data[i][1].replace('\n', '')
        df.iloc[i] = table_data[i][0:4]
    
    df = df[1:].reset_index(drop=True)
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape_and_display():
    data = scrape_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
```

そして、`templates/index.html` ファイルには、次のようなHTMLコードを記述します。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scraped Data Display</title>
</head>
<body>
    <h1>FDA Newly Added Guidance Documents</h1>
    {% if data is defined %}
    <table border="1">
        <tr>
            {% for col in data.columns %}
            <th>{{ col }}</th>
            {% endfor %}
        </tr>
        {% for row in data.values %}
        <tr>
            {% for val in row %}
            <td>{{ val }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    {% else %}
    <p>No data available. Click the button below to scrape.</p>
    {% endif %}
    <form action="/scrape" method="get">
        <button type="submit">Scrape Data</button>
    </form>
</body>
</html>
```

これで、Flaskアプリケーションが完成しました。サーバーを起動するには、ターミナルで `python app.py` を実行します。ブラウザで `http://127.0.0.1:5000/` にアクセスして、スクレイピングボタンをクリックすると、データが表示されます。