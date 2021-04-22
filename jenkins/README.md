# Jenkins

[Jenkins] is an open source automation server which enables developers around the world to reliably build, test, and deploy their software.

## Getting Started

使用 docker 建立 Jenkins 服務, 且將資料持久化.

### Container version

* jenkins/jenkins:2.277.3-alpine

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Build docker images and start container

```bash
make up
```

完成後, 瀏覽器開啟 `http://127.0.0.1` 會看到 Jenkins 介面, 初始密碼在 `data/secrets/initialAdminPassword`

### Stop Container

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

[Jenkins]: https://www.jenkins.io/
