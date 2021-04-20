# docker-redmine

Redmine 專案管理系統

## Getting Started

### Container version

* redmine:4.2.0

## Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## 使用方式

### Plugins

確認要開啟的 plugins, 如不需要就移除掉.

```bash
cd redmine/plugins
```

### Run services

```bash
make up
```

啟動完成後,在瀏覽器上開起 http://localhost 可看到 Redmine 畫面, 登入帳密如下

|角色|帳號|密碼|
|---|---|---|
|管理者|admin|admin|

### Stop services

```bash
make down
```

移除資料

```bash
make clean
```
