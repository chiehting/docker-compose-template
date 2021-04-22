FROM ruby:2.5.3-alpine3.8
LABEL maintainer "Justin Lee - <ting911111@gmail.com>"

RUN apk add --no-cache git openssh-client && \
    #gem install capistrano --version=3.10.1 && \
    gem install capistrano && \
    gem install dotenv && \
    gem install pulsar && \
    gem install capistrano-deploy_hooks && \
    rm -rf /var/cache/apk/*

