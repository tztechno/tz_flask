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
    
    n = 20
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
