from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_headlines(url, headline_tag, headline_text_tag=None):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all(headline_tag)
    if headline_text_tag:
        return [headline.find(headline_text_tag).get_text() for headline in headlines]
    else:
        return [headline.get_text() for headline in headlines]

@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/news/<site>')
def show_news(site):
    news_data = {
        'bbc': {
            'url': 'https://www.bbc.com/news',
            'headline_tag': 'h2'
        },
        'cnn': {
            'url': 'https://edition.cnn.com/',
            'headline_tag': 'span',
        }
        
    }

    if site in news_data:
        site_data = news_data[site]
        headlines = scrape_headlines(site_data['url'], site_data['headline_tag'], site_data.get('headline_text_tag'))
        return render_template('news.html', headlines=headlines, site=site)
    else:
        return f"No data for {site}"

if __name__ == '__main__':
    app.run(debug=True)