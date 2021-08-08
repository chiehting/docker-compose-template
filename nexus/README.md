# Nexus

[Nexus] is manage binaries and build artifacts across your software supply chain.

## Getting Started

使用 docker 建立 nexus repository 服務, 且將資料持久化.

### Container version

* sonatype/nexus3:3.30.0

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Build docker images and start

啟動時會建立nexus目錄, 並且給777權限.

```bash
make up
```

服務啟動後, 瀏覽器開啟 [http://localhost](http://localhost) 進入 Nexus, `admin` 帳戶的密碼位置在 `./data/admin.password`

### Stop container

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

[Nexus]: https://www.sonatype.com/products/repository-pro
