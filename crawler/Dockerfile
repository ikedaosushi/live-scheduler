FROM python:3.6.5

# ENV
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Workdir
WORKDIR /root/

# OS
RUN apt-get update \
    && apt-get install -y unzip graphviz

# Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \ 
    && apt-get update \ 
    && apt-get install -y google-chrome-stable

# ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \ 
    && mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION \ 
    && curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \ 
    && unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION \ 
    && rm /tmp/chromedriver_linux64.zip \ 
    && chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver \ 
    && ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver 

# Japanese
RUN wget -q http://ipafont.ipa.go.jp/old/ipafont/IPAfont00303.php -O IPAfont00303.zip  && \
    unzip IPAfont00303.zip -d /usr/share/fonts/ && fc-cache -fv && rm IPAfont00303.zip

# PyPI
ADD Pipfile Pipfile
RUN pip install -U pip \
    && pip install pipenv \
    && pipenv install --system --skip-lock
