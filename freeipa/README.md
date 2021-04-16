# freeipa

[Freeipa]  is an integrated security information management solution combining Linux (Fedora), 389 Directory Server, MIT Kerberos, NTP, DNS, Dogtag (Certificate System). It consists of a web interface and command-line administration tools.

## Getting Started



### version

* freeipa-server: centos-8-4.8.7

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running


變更環境變數

```bash
cat build/.env
REALM=CHIEHTING.COM
FREEIPA_PASSWORD=password
IPA_SERVER_HOSTNAME=ldap.chiehting.com
IPA_SERVER_IP=127.0.0.1
```

啟動服務

```bash
make dul
```

## Certificate

建立憑證

```bash
make cret
```

更新憑證

```bash
make rcret
```

[Freeipa]: https://www.freeipa.org/
