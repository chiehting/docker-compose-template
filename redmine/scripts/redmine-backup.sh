#!/bin/bash

set -x

cd `dirname $0`
S3=`hostname`
tarName=redmine-backup-`date "+%u"`.tar

tar zcfp ${tarName} /opt/docker-redmine
/bin/aws s3 cp ${tarName} s3://${S3}

rm -rf ${tarName}

echo 'done'
