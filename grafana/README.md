# Grafana

[Grafana] allows you to query, visualize, alert on and understand your metrics no matter where they are stored. Create, explore, and share dashboards with your team and foster a data driven culture.

## Getting Started

### Container version

* grafana/grafana:7.5.7

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 確認Makefile的任務

```bash
make help
```

### Modify environment file

```bash
cat build/.env
GF_SERVER_ROOT_URL=http://grafana.example
GF_SECURITY_ADMIN_USER=admin
GF_AUTH_DISABLE_LOGIN_FORM=false
GF_SECURITY_ADMIN_PASSWORD=password
GF_AUTH_LDAP_ENABLED=false # 需配置 data/conf/ldap.toml
```

### Build docker images and start

Start services of grafana

```bash
make up
```

瀏覽器開啟 [http://localhost](http://localhost) 即可以看到 Grafana 畫面.

### Stop Grafana

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

[Grafana]: https://grafana.com/
