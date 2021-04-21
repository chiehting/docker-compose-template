#!/bin/bash

echo "[ Start import sql process ]"

# Defined variables
export MYSQL_PWD=${MYSQL_ROOT_PASSWORD}
dir=$(cd "$(dirname "$0")";pwd)
logFileName="migration.log"

cd $dir
touch $logFileName

echo "[ Check MySQL can connect ]"
while ! mysql -uroot  -e ";" ; do
       echo -e "[ERROR]\tMySQL can't connected"
       exit 1
done

echo "[ RUN MySQL migration ]"
for migrateFileName in $(ls -1 | grep '\.sql$' | sort);
do

  record=$(grep -iR "${migrateFileName}" $logFileName)

  if [ -n "${record}" ];then
    echo -e "SKIP\t\t$record"
  else
    record="$(date '+%Y-%m-%d %H:%M:%S')\t$migrateFileName"
    echo -e "MIGRATE\t$record"
    mysql -uroot < $migrateFileName

    if [ $? -eq 0 ];then
      echo ${record} >> migration.log
    fi
  fi

done
