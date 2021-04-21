#!/bin/sh

function redis_service
{
    port=$1
    conf=$2
    mkdir -p /redis-conf/${port} /redis-data/${port}

    if [ -e /redis-data/${port}/nodes.conf ]; then
      rm /redis-data/${port}/nodes.conf
    fi

    sed 's/${port}/'${port}'/g' /data/${conf} > /redis-conf/${port}/redis_config.conf
    /usr/local/bin/redis-server /redis-conf/${port}/redis_config.conf
}

if [ "$mode" == 'cluster' ]; then
    conf=redis_cluster.conf.tmpl
    for port in `seq 7000 7005`; do
        redis_service ${port} ${conf}
    done

    sleep 1

    ip=$(getent hosts ${1:-$HOSTNAME} | awk '{print $1}')
    echo "yes" | ruby /usr/src/redis-trib.rb create --replicas 1 ${ip}:7000 ${ip}:7001 ${ip}:7002 ${ip}:7003 ${ip}:7004 ${ip}:7005

else
    port=6379
    conf=redis.conf.tmpl
    redis_service ${port} ${conf}
fi

tail -f /var/log/redis*.log

