# MySQL

[MySQL] Database Service is a fully managed database service to deploy cloud-native applications.

## Getting Started

### Container version

* mysql:8.0.24

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### start mysql service

預設為 MySQL 8.0.24, 若要使用其他版本可變更變數 `MYSQL_VERSION`

```bash
cat build/.env
# MYSQL_VERSION: 5.7.34
MYSQL_ROOT_PASSWORD: password
```

### Build docker images and start

啟動服務

```bash
make up
```

匯入 `./sql/*.sql` 檔案, 結果將並存留 `./sql/migration.log`

```bash
make sql
```

### Stop container

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

[MySQL]: https://www.mysql.com/
