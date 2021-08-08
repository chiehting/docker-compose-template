# HAProxy

[HAProxy] is a free, very fast and reliable solution offering high availability, load balancing, and proxying for TCP and HTTP-based applications.

## Getting Started

### Container Version

* haproxy:2.3.9-alpine

### Prerequisites

* [docker](https://docs.docker.com/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

## Running

### 確認Makefile的任務

```bash
make help
```

### Build docker images and start

建置docker images,並且啟動 container.

```bash
make up
```

Then you can hit [http://localhost](http://localhost) in your browser.

### Stop container

```bash
make down
```

[HAProxy]: http://www.haproxy.org/
