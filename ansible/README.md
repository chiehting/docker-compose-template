# Ansible

[Ansible] is an IT automation tool. It can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.

## Getting Started

使用 Docker 整合 Ansible 環境, 可以在 local 開發 roles 並且測試部署.

### Version

* Ansible: python3.7.3-alpine3.9

### Prerequisites

* [docker]
* [docker-compose]

## Running

Show Makefile list of targets

```bash
bash-3.2$ make
ps     docker-compose ps
du     docker-compose down and up
dul    docker-compose down and up and logs
```

Build docker images and start

```bash
bash-3.2$ make du
```

Run hello_world playbooks

```bash
docker exec -it ansible ansible-playbook -i inventories playbooks/hello_world.yml 
```

[Ansible]: https://github.com/ansible/ansible
[docker]: https://docs.docker.com/install/
[docker-compose]: https://docs.docker.com/compose/install/