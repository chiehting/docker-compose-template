# Gitlab

建立 Gitalb

## Getting Started

配置基本設定

* [GitLab Pages administration](https://docs.gitlab.com/ce/administration/pages/)

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 確認Makefile的任務

```bash
make
```

### Build docker images and start

Build the docker image, and start services of gitlab-server、gitlab-runner

```bash
make up
```

### Register gitlab runner

註冊 gitlab runner 到 gitlab 中

```bash
make register
```
