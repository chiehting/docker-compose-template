#!/bin/bash

# TDengine 災害還原腳本
BACKUP_DIR="/backup"
RESTORE_DATE=$1

if [ -z "$RESTORE_DATE" ]; then
    echo "使用方法: $0 <備份日期> (格式: YYYYMMDD_HHMMSS)"
    echo "可用備份:"
    ls -la "$BACKUP_DIR/daily/"*.tar.gz 2>/dev/null | awk '{print $9}' | sed 's/.*\///' | sed 's/\.tar\.gz$//'
    exit 1
fi

BACKUP_FILE="$BACKUP_DIR/daily/$RESTORE_DATE.tar.gz"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "錯誤: 備份文件不存在 - $BACKUP_FILE"
    exit 1
fi

echo "警告: 這將覆蓋現有數據！"
read -p "確定要繼續嗎? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "還原已取消"
    exit 0
fi

echo "$(date): 開始還原 TDengine 數據..."

# 停止 TDengine 服務
docker-compose stop tdengine-node1 tdengine-node2 tdengine-node3

# 解壓備份
cd "$BACKUP_DIR/daily"
tar -xzf "$RESTORE_DATE.tar.gz"

# 還原數據
for node in dnode1 dnode2 dnode3; do
    if [ -d "$RESTORE_DATE/$node" ]; then
        echo "還原 $node 數據..."
        rsync -av --delete "$RESTORE_DATE/$node/" "/opt/tdengine/data/$node/data/"
    fi
done

# 清理臨時文件
rm -rf "$RESTORE_DATE"

# 重啟服務
docker-compose up -d

echo "$(date): 還原完成"