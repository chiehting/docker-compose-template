# MariaDB

[MariaDB] Server is one of the most popular open source relational databases.

## Getting Started

### Container version

* mariadb:10.5.9

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Modify environment file

```bash
cat build/.env
MYSQL_ROOT_PASSWORD=password
# If you want ceate mariadb cluster, please set variables MARIADB_CLUSTER=true
MARIADB_CLUSTER=false
```

### Build docker images and start container

```bash
make up

# mariadb info
user=root
pass=password
docker exec -it marisdb mysql -u"${user}" -p"${pass}" -e "SHOW DATABASES";
docker exec -it marisdb mysql -u"${user}" -p"${pass}" -e "SHOW GLOBAL STATUS LIKE 'wsrep_%'";
```

### Stop Container

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

[MariaDB office]: https://mariadb.org/
