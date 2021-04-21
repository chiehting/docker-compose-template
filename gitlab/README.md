# Gitlab

[GitLab] is the open DevOps platform, delivered as a single application. 

## Getting Started

1. 將啟動 Gitalb + Gitlab Runner
2. 為了避免 `File name too long` 問題, volume 路徑使用 d (data) 當作名稱.
3. 設定檔配置請參考 [GitLab Pages administration](https://docs.gitlab.com/ce/administration/pages/).

### Container version

* gitlab-ce:13.4.1-ce.0

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
EXTERNAL_URL=127.0.0.1
GITLAB_PAGES_URL=127.0.0.1
LETSENCRYPT_ENABLE=false # 若要自動申請憑證則開啟, 必須要綁定 Domain Name 做認證
REDIRECT_HTTP_TO_HTTPS=false
```

### Build docker images and start

Start services of gitlab-server、gitlab-runner

```bash
make up
```

瀏覽器開啟 `http://localhost` 即可以看到 Gitlab 畫面.

### Stop Gitlab

停止服務

```bash
make down
```

移除資料

```bash
make clean
```

### Register Gitlab Runner

註冊 gitlab runner 到 gitlab 中

```bash
make register
```

## Troubleshoot

### File name too long

由於 MacOS 有 File Name 限制, 在使用 Volume 時若超過 MacOS 限制時會出現 `File name too long` 的錯誤, 詳細限制可以參考討論 https://discussions.apple.com/thread/8079993 .

解決方法:

可以移除或縮短 `build/docker-compose.yml` 內 `volume`.


[GitLab]: https://about.gitlab.com/
