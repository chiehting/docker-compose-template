#!/bin/bash

# TDengine 備份腳本
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=${RETENTION_DAYS:-14}

# 創建備份目錄
mkdir -p "$BACKUP_DIR/daily/$DATE"

echo "$(date): 開始備份 TDengine 數據..."

# 備份數據文件
for node in dnode1 dnode2 dnode3; do
    if [ -d "/source/$node" ]; then
        echo "備份 $node 數據..."
        rsync -av "/source/$node/" "$BACKUP_DIR/daily/$DATE/$node/"
    fi
done

# 壓縮備份
cd "$BACKUP_DIR/daily"
tar -czf "$DATE.tar.gz" "$DATE"
rm -rf "$DATE"

# 清理舊備份
find "$BACKUP_DIR/daily" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "$(date): 備份完成 - $BACKUP_DIR/daily/$DATE.tar.gz"

# 備份驗證
if [ -f "$BACKUP_DIR/daily/$DATE.tar.gz" ]; then
    echo "$(date): 備份驗證成功"
    # 可以在這裡添加上傳到雲存儲的邏輯
else
    echo "$(date): 備份驗證失敗" >&2
    exit 1
fi