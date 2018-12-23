import os, sys, re, datetime, time
from dateutil.relativedelta import relativedelta

from requests_html import HTML

import browser
import dynamo

def aggregate(event, context):
    today = datetime.datetime.today()
    endpoint = 'https://www-shibuya.jp/schedule/#wwwxwww/'

    driver = browser.get_browser()
    driver.get(endpoint)
    time.sleep(3)

    ls_events = []
    for i in range(3): # 3ヶ月分
        current_date = today + relativedelta(month=i)
        year = current_date.year
        month = current_date.month
        
        html = HTML(html=driver.page_source, url='')
        articles = html.find('#eventList > div > article')
        for article in articles:        
            day = int(article.find('.date .day', first=True).text)
            datetime_ = datetime.date(year, month, day)

            url = article.find('.pageLink', first=True).attrs.get('href')
            place = article.find('.inner .placeLabel span', first=True).text
            artist = article.find('.inner .info .title', first=True).text
            title = article.find('.inner .info .exp span', first=True).text
            openstart = article.find('.inner .info .openstart', first=True).text
            oss = openstart.replace('OPEN / START\u3000', '').split('/')
            if len(oss) == 2:
                open_, start = oss

            dic_event = {
                'datetime': datetime_, 'url': url, 'place': place, 'artist': artist, 'title': title,
                'open': open_, 'start': start, 'open_start': oss
            }
            ls_events.append(dic_event)
        next_button = driver.find_element_by_css_selector('#schedule > * > ul > li.next > a')
        next_button.click()

    driver.close()
    driver.quit()

    items = process_to_items(ls_events)
    dynamo.put_items(items)

    response = {
        "statusCode": 200,
        "body": f"{len(ls_events)} items added or updated"
    }

    return response

def process_to_items(ls_events):
    items = []
    for event in ls_events:
        id_ = "{}_{}".format(event['place'].lower().replace(' ', ''), event['datetime'].strftime('%Y%m%d'))
        item = {
            'id': id_,
            'title': event['title'],
            'date': event['datetime'].strftime('%Y-%m-%d'),
            'place': event['place'], 
            'artist': event['artist'],
            'open': event['open'],
            'start': event['start']
        }

        items.append(item)

    return items