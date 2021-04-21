FROM redis:5.0.8-alpine
MAINTAINER Chiehting

ADD https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64 /usr/local/bin/dumb-init

COPY ./redis.conf.tmpl /data/
COPY ./redis_cluster.conf.tmpl /data/
COPY ./redis-trib.rb /usr/src/
COPY ./docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/dumb-init /usr/local/bin/docker-entrypoint.sh && \
    apk --no-cache add ruby && \
    echo 'gem: --no-document' > /etc/gemrc && \
    gem install rdoc && \
    gem install redis -v 4.1.3

EXPOSE 6379 7000  7001 7002 7003 7004 7005
ENTRYPOINT ["dumb-init"]
CMD ["docker-entrypoint.sh"]
