#!/bin/bash

printf "\n$ELASTICSEARCH_PASSWORD" | /usr/share/elasticsearch/bin/elasticsearch-certutil ca
mv /usr/share/elasticsearch/elastic-stack-ca.p12 /usr/share/elasticsearch/config/certs/

exit 0
