import os, sys, re, logging
from datetime import date
from pathlib import Path

from requests_html import HTMLSession
import pandas as pd

pj_dir = Path(__file__).parents[1]
data_dir = pj_dir/'data'
src_dir = pj_dir/'src'
sys.path.append(str(src_dir))


from datetime import date
class Event():
    def __init__(self):
        self.year = 2000
        self.month = 1
        self.day = 1
        self.title = ''
        self.artist = ''
        self.description = ''
        self.url = ''
        self.open_ = ''
        self.start = ''
        self.place = ''
        
    @property
    def date(self):
        return date(self.year, self.month, self.day)
    
    def tolist(self):
        return [self.place, self.title, self.artist, self.description, self.url, self.date, self.open_, self.start]


def main():
    events = get_events()
    columns = ['place', 'title', 'artist', 'description', 'url', 'date', 'open_', 'start']
    df = pd.DataFrame([e.tolist() for e in events], columns=columns)

    outputpath  = data_dir/'live/201806_www.csv'
    df.to_csv(outputpath)
    logging.info("export to %s!", str(outputpath))


def get_events():
    sess = HTMLSession()
    r = sess.get('http://www-shibuya.jp/schedule/#wwwxwww/201806')
    articles = r.html.find('#eventList > div > article')
    events = []
    for article in articles:
        event = Event()
        event.url = article.find('.pageLink', first=True).attrs.get('href', '')
        event.year = 2018
        event.month = 6
        event.day = int(article.find('.inner .event .date .day', first=True).text)
        event.place = article.find('.inner .placeLabel span', first=True).text
        event.artist = article.find('.inner .info .title', first=True).text
        event.title = article.find('.inner .info .exp span', first=True).text
        openstart = article.find('.inner .info .openstart', first=True).text
        oss = openstart.replace('OPEN / START\u3000', '').split('/')
        if len(oss) == 2:
            event.open_, event.start = oss

        events.append(event)

    return events


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s- %(name)s - %(levelname)s - %(message)s')
    main()