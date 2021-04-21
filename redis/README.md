# redis

建立 redis, redis cluster 環境.

## Getting Started

用於開發環境, 並提供 redislabs web gui 介面做資料查詢.

### Container version

* redislabs/redisinsight:1.10.0
* redis:5.0.8-alpine

### Prerequisites

1. Installed [docker](https://docs.docker.com/install/) engine.
2. Indtalled [docker-compose](https://docs.docker.com/compose/) tool.

## Running

### Modify environment file

預設為 single, 若有使用群集模式可以開啟配置 `MODE=culster`

```bash
cat build/.env
# MODE=cluster
```

### Build docker images and start

啟動服務

```bash
make up
```

服務啟動後, 瀏覽器開啟 http://localhost 進入 redisinsight, 輸入下面資訊

|key|single|cluster|
|---|---|---|
|Host|redis|redis|
|Port|6379|7000|
|Host|single|cluster|

### Stop container

停止服務

```bash
make down
```

移除資料

```bash
make clean
```
