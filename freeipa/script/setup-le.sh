#!/usr/bin/bash

echo "#############################"
echo "## Start setup letsencrypt ##"
echo "#############################"

set -o nounset -o errexit

FQDN=$(hostname -f)
WORKDIR=$(dirname "$(realpath $0)")
CERTS=("isrgrootx1.pem" "isrg-root-x2.pem" "lets-encrypt-r3.pem" "lets-encrypt-e1.pem" "lets-encrypt-r4.pem" "lets-encrypt-e2.pem")

echo "## Install package"
yum install epel-release mod_ssl -y
yum install certbot -y

if [ ! -d "/etc/ssl/$FQDN" ]
then
    mkdir -p "/etc/ssl/$FQDN"
fi

echo "## Install root certificates"
for CERT in "${CERTS[@]}"
do
    if command -v wget &> /dev/null
    then
        wget -O "/etc/ssl/$FQDN/$CERT" "https://letsencrypt.org/certs/$CERT"
    elif command -v curl &> /dev/null
    then
        curl -o "/etc/ssl/$FQDN/$CERT" "https://letsencrypt.org/certs/$CERT"
    fi
    ipa-cacert-manage install "/etc/ssl/$FQDN/$CERT"
done

echo "## Update ipa cert"
ipa-certupdate

echo "## Finish setup letsencrypt"

"$WORKDIR/renew-le.sh" --first-time
