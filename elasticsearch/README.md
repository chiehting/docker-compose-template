# haproxy

建立 elasticsearch 

## Getting Started

elasticsearch + kibana

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 初始化

建立相關資料夾以及憑證

1. 變更密碼

```bash
vim elasticsearch-certutil.yml
...
ELASTICSEARCH_PASSWORD: "password"
...

vim docker-compose.yml
...
xpack.security.transport.ssl.keystore.password=password
xpack.security.transport.ssl.truststore.password=password
ELASTIC_PASSWORD=password
ELASTICSEARCH_PASSWORD: "password"
...
```

2. 初始化

會在生成憑證 "`certs/elastic-stack-ca.p12`"

```
make init
```

### 啟動服務

確認憑證 "`certs/elastic-stack-ca.p12`" 存在後, 即可啟動服務

```bash
# down and up
make du

# view log
make logs

# down
make down
```

Then you can hit `http://localhost` in your browser through default account "`elastic/password`"

### 管理用戶

```
# create user
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-users useradd justin -p 123456 -r superuser

# delete user
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-users userdel justin
```

 




