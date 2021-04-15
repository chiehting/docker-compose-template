# docker-redmine

Redmine 系統

## Prerequisites

1. Installed docker engine.
2. Installed docker-compose tool.

## 使用方式

確認要開啟的 plugins, 如不需要就移除掉.

```bash
cd redmine/plugins
```

Redmine 服務啟動.

```bash
docker-compose up -d
```

## 系統帳號

|角色|帳號|密碼|
|---|---|---|
|管理者|admin|admin|