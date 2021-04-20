#!/bin/bash

set -x

cd `dirname $0`
S3=`hostname`

/bin/gitlab-ctl backup-etc
/bin/gitlab-backup create SKIP=artifacts,builds

tar zcfp gitlab-backup-`date "+%u"`.tar /etc/gitlab/config_backup /var/opt/gitlab/backups
/bin/aws s3 cp gitlab-backup-`date "+%u"`.tar s3://${S3}

rm -rf gitlab-backup-`date "+%u"`.tar /etc/gitlab/config_backup/* /var/opt/gitlab/backups/*

echo 'done'
