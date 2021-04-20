# OpenVPN

OpenVPN Server

基於 Github 專案 [docker-openvpn](https://github.com/kylemanna/docker-openvpn)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Modify environment file

```bash
cat build/.env
DOMAINNAME=VPN.SERVERNAME.COM
```

### Build docker images and start

初始化, 建立相關資料夾以及憑, 憑證會生成在 "`data`" 底下

```bash
make init
```

啟動服務

```bash
make up
```

建立用戶, 用戶憑證會生成在 "`data/justin.ovpn`"

```bash
make client user=justin
```

### Stop container

停止服務

```bash
make down
```

移除資料

```bash
make clean
```
