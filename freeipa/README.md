# docker-ansible

建立freeipa服務.

## Getting Started

使用官方 freeipa image 建置 freeipa 服務, 並使用腳本更新憑證.

* [freeipa](https://hub.docker.com/r/freeipa/freeipa-server/)

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

編輯 dcoker-compose.yml 裡面參數 PASSWORD、hostname、IPA_SERVER_HOSTNAME


啟動服務

```bash
docker-compose up -d
```

建立憑證

```bash
docker exec -it freeipa bash

# 取得認證
printf "$PASSWORD"|kinit admin
klist

# 更新管理 CA  root certificates
/script/setup-le.sh
```

更新憑證

```bash
docker exec -it freeipa /script/renew-le.sh
```

