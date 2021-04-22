# Capistrano

[Prometheus] is an open-source systems monitoring and alerting toolkit originally built at SoundCloud.

## Getting Started

整合 Prometheus、node_exporter、Grafana, 可以在 local 開發與測試.

Prometheus 提供不少 [exporters](https://prometheus.io/docs/instrumenting/exporters/) 使用

### Container version

* quay.io/prometheus/prometheus:v2.26.0
* quay.io/prometheus/node-exporter:v1.1.2
* grafana/grafana:7.5.4

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Build docker images and start

```bash
make up
```

啟動完成後

1. 在瀏覽器上開起連結 `http://127.0.0.1` 進入 Grafana, 使用帳號 `admin` 密碼 `admin` 登入
2. 在瀏覽器上開起連結 `http://127.0.0.1:9090/targets`, 進入 Prometheus UI, 顯示目前所有 targets 狀態
3. 在瀏覽器上開起連結 `http://127.0.0.1:9100/metrics`, 近入 node exporter, 顯示 Container 的 metric

### Stop container

```bash
make down
```

清除資料

```bash
make clean
```

[Prometheus]: https://prometheus.io/
