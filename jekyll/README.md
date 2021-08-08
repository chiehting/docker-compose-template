# Jekyll

[Jekyll] is a static site generator. It takes text written in your favorite markup language and uses layouts to create a static website.

## Getting Started

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

Then you can hit [http://localhost](http://localhost) in your browser.

### Stop container

```bash
make down
```

[Jekyll]: https://jekyllrb.com/
