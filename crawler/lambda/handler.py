import os, sys, re, datetime, time
from dateutil.relativedelta import relativedelta

from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def hello(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)

    driver.get('https://blog.ikedaosushi.com/')
    body = f"Blog title is: {driver.title}"

    driver.close();
    driver.quit();

    response = {
        "statusCode": 200,
        "body": body
    }

    return response