import xml.etree.ElementTree as ET
import requests
from flask import Flask, render_template, request, redirect, url_for
from config.podcasts_list import PODCASTS

app = Flask(__name__)

@app.route('/load_xml/<url>', methods=['GET'])
def load_xml(url):
    print("Load XML Endpoint Executed") # Debugging statement
    response = requests.get(url)
    xml_data = response.content

    root = ET.fromstring(xml_data)

    # Get the podcast title
    title = root.find('channel/title').text

    # Get the list of episodes
    episodes = []
    for item in root.findall('channel/item'):
        date = item.find('pubDate').text
        episode_title = item.find('title').text
        episodes.append((date, episode_title))

    return render_template('index.html', title=title, episodes=episodes, podcasts=PODCASTS)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        response = requests.get(url)
        xml_data = response.content

        root = ET.fromstring(xml_data)

        # Get the podcast title
        title = root.find('channel/title').text

        # Get the list of episodes
        episodes = []
        for item in root.findall('channel/item'):
            date = item.find('pubDate').text
            episode_title = item.find('title').text
            episodes.append((date, episode_title))

        return render_template('index.html', title=title, episodes=episodes, podcasts=PODCASTS)

    return render_template('index.html', podcasts=PODCASTS)

if __name__ == '__main__':
    app.run(debug=True)
