# freeipa

[Freeipa]  is an integrated security information management solution combining Linux (Fedora), 389 Directory Server, MIT Kerberos, NTP, DNS, Dogtag (Certificate System). It consists of a web interface and command-line administration tools.

## Getting Started

FreeIPA 需要 volumes cgroup, 所以只能在 Linux 上執行. 目前已確認下列版本可以使用

* Centos7
* Centos8
* Ubuntu 18.16
* Ubunut 20.04

### Container version

* freeipa-server:centos-8-4.8.7

### Prerequisites

* [cgroup](https://man7.org/linux/man-pages/man7/cgroups.7.html)
* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 變更環境變數

```bash
cat build/.env
REALM=CHIEHTING.COM
FREEIPA_PASSWORD=password
IPA_SERVER_HOSTNAME=ldap.chiehting.com
IPA_SERVER_IP=127.0.0.1
```

### 啟動服務

```bash
make up
```

瀏覽器開啟 `http://localhost` 即可以看到 FreeIPA 畫面.

### 停止服務

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

## Certificate

建立憑證, 必須要配置 Domain 才能做認證

```bash
make cret
```

更新憑證

```bash
make rcret
```

[Freeipa]: https://www.freeipa.org/
