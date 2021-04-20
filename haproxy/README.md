# haproxy

建立 haproxy 

## Getting Started

建立 haproxy 做反向代理

### Container Version

* haproxy:2.3.9-alpine

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 確認Makefile的任務

```bash
make help
```

### Build docker images and start

1. 建置docker images,並且啟動 container.

```bash
make up
```

2. Then you can hit `http://localhost` in your browser.

### Stop container

```bash
make down
```
