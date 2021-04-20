# docker-jekyll

使用docker建立jekyll環境

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Container version

* ruby:2.7.2-alpine3.13
* jekyll:2.6.1-alpine3.9

### Prerequisites

* We need own [Jekyll](https://jekyllrb.com/docs/) site.
* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

Use [jekyll-theme-next](https://github.com/simpleyyt/jekyll-theme-next) themes.

### Build docker images and start

```bash
make up
```

Then you can hit `http://localhost` in your browser.

### Stop container

```bash
make down
```
