# PHP

[PHP] is a popular general-purpose scripting language that is especially suited to web development.

## Getting Started

PHP + Nginx 開發環境

### Container version

* php:7.4.2-fpm-alpine3.13
* nginx:1.19.10-alpine

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### Nginx setting

編輯 `nginx/config/default.conf` 可以配置路由, 預設 `.php` 檔案則讓 php fpm 處理

```bash
location ~ (.php)$ {
    fastcgi_pass   php:9000;
    fastcgi_index  index.php;
    fastcgi_param  SCRIPT_FILENAME  /var/www/html/$fastcgi_script_name;
    include        fastcgi_params;
```

### Build docker images and start

```bash
make up
```

服務啟動後, 瀏覽器開啟 [localhost](http://localhost/index.php) 會看到 `hello world`

### Stop container

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

[PHP]: https://www.php.net/
