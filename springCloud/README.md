# Spring Cloud

[Spring Cloud] provides tools for developers to quickly build some of the common patterns in distributed systems (e.g. configuration management, service discovery, circuit breakers, intelligent routing, micro-proxy, control bus, one-time tokens, global locks, leadership election, distributed sessions, cluster state).

## Getting Started

Spring Cloud 官方套件可參考下面連結

* [spring-cloud projects](https://spring.io/projects/spring-cloud)

目前範例使用了

* [Spring Cloud Config](https://spring.io/projects/spring-cloud-config)
* [Spring Cloud Netflix (Eureka)](https://spring.io/projects/spring-cloud-netflix)
* [Spring Cloud Gateway](https://spring.io/projects/spring-cloud-gateway)

### Container version

* openjdk:8u201-jdk-alpine3.9
* maven:3.6.2-jdk-11

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Build Java package

編譯 Java 服務 webclient、webservice、gateway、eureka、config

```bash
make build-all
```

### Start container

```bash
make up
```

啟動完成後

1. 在瀏覽器上開起連結 `http://127.0.0.1:88` 進入 eureka 介面, 可以看到已註冊的服務
2. 在瀏覽器上開起連結 
    * `http://127.0.0.1:81/neo-config/pro/master` 可以看到 config `neo-config-pro.properties`
    * `http://127.0.0.1:81/neo-config/test/master` 可以看到 config `neo-config-test.properties`
    * `http://127.0.0.1:81/neo-config/dev/master` 可以看到 config `neo-config-dev.properties`
    
    
    這邊使用範例 [config-repo](https://github.com/ityouknow/spring-cloud-examples/tree/master/config-repo), 相關配置在 `./config/src/main/resources/bootstrap.yml`

3. 在瀏覽器上開起連結 
    * `http://127.0.0.1/` 可以看到 webclient 的 Hello Page
    * `http://127.0.0.1/hello` 可以看到 webservice 的計數器回傳 `{"message":"Hi there! you are number 1"}`

### Stop container

```bash
make down
```

清除資料

```bash
make clean
```

[Spring Cloud]: https://spring.io/projects/spring-cloud
