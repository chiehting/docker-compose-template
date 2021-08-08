# Elasticsearch

[Elasticsearch] is a distributed, RESTful search and analytics engine capable of addressing a growing number of use cases.

## Getting Started

Elasticsearch + Kibana

### Container version

* elasticsearch:7.12.0

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Modify environment file

```bash
cat build/.env
ELASTICSEARCH_PASSWORD=password
```

### Build docker images and start

初始化, 建立相關資料夾以及憑, 憑證會生成在 "`certs/elastic-stack-ca.p12`" 底下

```bash
make init
```

確認憑證 "`certs/elastic-stack-ca.p12`" 存在後, 即可啟動服務

```bash
# Containers down and up and logs
make dul
```

瀏覽器開啟 [http://localhost](http://localhost) 即可以看到 Kibana 畫面, 使用者帳號 "`elastic` 密碼為剛剛設置的密碼 "`password`"

### Stop containers

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

## 管理用戶

建立帳號 justin 的 superuser

```bash
# create user
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-users useradd justin -p 123456 -r superuser
```

移除帳號 justin

```bash
# delete user
docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-users userdel justin
```

 [Elasticsearch]: https://www.elastic.co/elasticsearch/