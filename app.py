#import sys
#sys.path.append('/var/www/py-podcast-site/config')

import xml.etree.ElementTree as ET
import requests
import datetime
from flask import Flask, render_template, request, redirect, url_for
#from config.podcasts_list import PODCASTS
PODCASTS = [
    'http://podcasternews.com/feed/',
    'https://www.techlifepodcast.com/podcast-feed.xml',
    'http://origin.podnews.net/rss/',
    'http://feeds.feedburner.com/ThisWeekInPodcasting',
    'https://theaudacitytopodcast.com/feed/'
]

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    data = {}

    if request.method == 'POST':
        url = request.form['url']
        response = requests.get(url)
        xml_data = response.content

        root = ET.fromstring(xml_data)

        data["title"] = root.find('channel/title').text
        data["image_url"] = root.find('channel/image/url').text
        data["description"] = root.find('channel/description').text

        # Get the list of episodes
        data["episodes"] = []
        for item in root.findall('channel/item'):
            date = item.find('pubDate').text
            try:
                date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
                date = date.strftime("%B %d, %Y")
            except ValueError:
                date = "Invalid Date"
            episode_title = item.find('title').text
            data["episodes"].append((date, episode_title))

    return render_template('index.html', podcasts=PODCASTS, data=data)

@app.route('/remove_data', methods=['GET'])
def remove_data():
    data = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
