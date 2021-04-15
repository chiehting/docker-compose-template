# ansible

ansible 環境.

## Getting Started

使用docker整合ansible環境,可以在local開發roles並且測試部署是否成功.

* [ansible](https://github.com/ansible/ansible)

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 確認Makefile的任務

```bash
make
```

### Build docker images and start

建置docker images,並且up.

```bash
make up
```

```bash
docker exec -it ansible ansible-playbook -i inventories playbooks/hello_world.yml 
```

