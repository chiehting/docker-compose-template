# AWX

[AWX] provides a web-based user interface, REST API, and task engine built on top of Ansible. It is the upstream project for Tower, a commercial derivative of AWX.

## Getting Started

* [awx](https://www.ansible.com/products/awx-project)
* [github awx](https://github.com/ansible/awx)

### Container version

* ansible/awx:15.0.1
* ansible/awx:15.0.1
* redis:6.2.2-alpine3.13
* postgres:10

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 確認變數

```bash
cat data/environment.sh
DATABASE_USER=awx
DATABASE_NAME=awx
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_PASSWORD=awxpass
AWX_ADMIN_USER=admin
AWX_ADMIN_PASSWORD=password
```

### Build docker images and start

```bash
make up
```

啟動後, 在瀏覽器上開起連結 `http://127.0.0.1` 進入 AWX 介面, 預設帳號 `admin` 密碼 `password`

### Stop container

```bash
make down
```

移除資料

```bash
make clean
```

[AWX]: https://github.com/ansible/awx
