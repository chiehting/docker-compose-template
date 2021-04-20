#!/usr/bin/bash
echo "########################"
echo "### Start renew cert ###"
echo "########################"

set -o nounset -o errexit
WORKDIR=$(dirname "$(realpath $0)")

### cron
# check that the cert will last at least 2 days from now to prevent too frequent renewal
# comment out this line for the first run
if [ "${1:-renew}" != "--first-time" ]
then
    start_timestamp=`date +%s --date="$(openssl x509 -startdate -noout -in /var/lib/ipa/certs/httpd.crt | cut -d= -f2)"`
    now_timestamp=`date +%s`
    let diff=($now_timestamp-$start_timestamp)/86400
    if [ "$diff" -lt "2" ]; then
        echo "## Create cert will last at least 2 days from now to prevent too frequent renewal"
        exit 0
    fi
fi
cd "$WORKDIR"

# httpd process prevents letsencrypt from working, stop it
echo "## Httpd process prevents letsencrypt from working, stop it"
systemctl stop httpd

# get a new cert
echo "## Get a new cert"
certbot certonly --standalone -w /var/www/html -d ${IPA_SERVER_HOSTNAME} --register-unsafely-without-email --agree-tos --force-renewal

# replace the cert
echo "## Replace the cert"
printf "\n\n"|ipa-server-certinstall -w -d /etc/letsencrypt/live/${IPA_SERVER_HOSTNAME}/privkey.pem /etc/letsencrypt/live/${IPA_SERVER_HOSTNAME}/cert.pem
restorecon -v /var/lib/ipa/certs/httpd.crt

# start httpd with the new cert
echo "## Start httpd with the new cert"
systemctl start httpd

echo "## Finish renew cert."
