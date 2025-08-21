apk add --no-cache dcron gnupg &&
echo '0 2 * * * /backup.sh' | crontab - &&
crond -f -d 8