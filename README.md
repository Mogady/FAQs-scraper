# FAQ scraper

## Introduction
This project using Scrapy tool to scrap FAQs from companies' helpCenters.

## Build the docker image

To build the image run:
```bash
$ docker build -t scraping.
```

## Run spider
```bash
$ docker run scraping spider-name
```
#### to run one of the examples
```bash
$ docker run scraping zappos
```
### Extra
you can use Mongodb pipeline, by simply changing the pipelines in settings.py
