# This Dockerfile builds the server only.

###########
# BUILDER #
###########
# pull official base image
FROM python:3.10-slim-buster as builder
# set work directory
WORKDIR /usr/src/app/server
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc
# lint
RUN pip install --upgrade pip
RUN pip install flake8==3.9.1
COPY ./server/ /usr/src/app/server/
RUN flake8 --exclude __init__.py --ignore=T001,T003,E402,W503,B001,E712,E262,382,495,F841,E711,N801,N806,C901,E722 ./ --max-line-length=250
# install python dependencies
COPY ./requirements.txt requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/server/wheels -r requirements.txt


#########
# FINAL #
#########
# pull official base image
FROM python:3.10-slim-buster
# create the app user
RUN addgroup --system app && adduser --system --group app
# create the appropriate directories
ENV HOME=/home/app/
ENV SERVER_HOME=$HOME/server/
RUN mkdir $SERVER_HOME
WORKDIR $SERVER_HOME
# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
RUN apt-get install curl -y
COPY --from=builder /usr/src/app/server/wheels /wheels
COPY --from=builder /usr/src/app/server/requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*
RUN apt-get install wget -y
RUN apt-get update && apt-get install -y gnupg2
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# set display port to avoid crash
ENV DISPLAY=:99
# install selenium
RUN pip install selenium==3.8.0
# COPY server/migrations $SERVER_HOME/migrations
COPY ./server/app.py $SERVER_HOME
COPY ./server/database.json $SERVER_HOME
COPY ./server/corpus.json $SERVER_HOME
COPY ./server/important_words.json $SERVER_HOME
COPY ./server/templates/ $SERVER_HOME/templates/
# chown all the files to the app user
RUN chown -R app:app $SERVER_HOME
# change to the app user
USER app
EXPOSE 5000
ENTRYPOINT ["python3", "-u", "app.py", "--host", "0.0.0.0", "--port", "5000"]
# ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]