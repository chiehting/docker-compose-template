#!/bin/bash

MARIADB_CLUSTER=$(echo "$MARIADB_CLUSTER" | tr '[:upper:]' '[:lower:]')
MARIADB_GALERA_FILE=galera.cnf

if [ "${MARIADB_CLUSTER}" == "true" ]
then
  echo  "## run MariaDB cluster"
  cp -f /build/${MARIADB_GALERA_FILE} /etc/mysql/conf.d/${MARIADB_GALERA_FILE}
  docker-entrypoint.sh mysqld --wsrep-new-cluster
else
  echo  "## run MariaDB"
  docker-entrypoint.sh mysqld
fi
