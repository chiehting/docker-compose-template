# git-repo

config server 使用本地 git

1. 編輯 `./config/src/main/resources/bootstrap.yml`, 變更 `uri: file://opt/src/git-repo`
2. 進入 `./config/git-repo`
3. 初始化 git

```bash
git init
```

4. 加入 `config-repo, 並做 git commit

```bash
git add .
git commit -m 'first commit'
```