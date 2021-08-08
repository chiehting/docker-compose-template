# Capistrano

[Capistrano] is a remote server automation tool.

## Getting Started

使用 docker 整合 Captriano + pulsar, 可以在 local 開發 tasks 並且測試部署是否成功.

Pulsar allows you to run Capistrano tasks via a separate repository where all your deploy configurations are stored.

* [capistrano](https://github.com/capistrano/capistrano)
* [pulsar](https://github.com/nebulab/pulsar)

### Container version

* ruby:2.5.3-alpine3.8

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Build docker images and start

```bash
make up
```

### Deploy Setting

編輯 `data/apps/docker-compose-template/deploy.rb` 設定部署專案

```bash
cat data/apps/docker-compose-template/deploy.rb

set :application, 'docker-compose-template'
set :repo_url, 'https://github.com/chiehting/docker-compose-template.git'
ask :branch, 'main'
set :deploy_to, '/opt/docker-compose-template' # deploy to remote host path
```

編輯 `data/apps/docker-compose-template/production.rb` 設定遠端主機

```bash
cat data/apps/docker-compose-template/production.rb

server 'remoteHost', user: 'root', roles: %w{web app db}, primary: true
set :stage, :production # 定義 stage 變數
```

### Deploy project to remoteHost container

從 `capistrano` 部署專案至 `remoteHost`

```bash
# 確保 id_rsa 權限正確
docker exec -it capistrano chmod 0600 /root/.ssh/id_rsa

# 部署專案
docker exec -it capistrano pulsar deploy docker-compose-template production
```

確認是否部署至 `remoteHost`

```bash
docker exec -it remoteHost ls /opt/docker-compose-template
```

### Run tasks

call helloworld to print hello world, 任務程式在 `./data/recipes`

```bash
docker exec -it capistrano pulsar task docker-compose-template production tests:helloworld
Resolving dependencies...
The Gemfile's dependencies are satisfied
hello world
Executed task tests:helloworld for docker-compose-template on production!
```

### Stop container

```bash
make down
```

[Capistrano]: https://capistranorb.com/
