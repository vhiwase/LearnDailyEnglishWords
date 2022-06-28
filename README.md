# LearnDailyEnglishWords
This repo is created to learn some english words with image scraping

## Commands to Run

```sh
docker-compose up --build -d
docker-compose down -v
```

## Docker Image
DockerHub https://hub.docker.com/repository/docker/sad123/learn-daily-english-words

## Access Application Online
Hosted on Azure Container App with CI/CD and OAuth security
Link of Application: https://learn-daily-english-words.delightfulforest-b9dc5d98.eastasia.azurecontainerapps.io

## Generate database for quick loading
Make sure you first intall depedencies from [blog post](https://testdriven.io/blog/building-a-concurrent-web-scraper-with-python-and-selenium/).

Then Run the following command to quickly load vocabulary words:
```sh
python3 server/database.py
```

Alternatively you can use docker compose commands:
```sh
docker-compose -f docker-compose.database.yml up --build -d
docker-compose -f docker-compose.database.yml down -v
```
