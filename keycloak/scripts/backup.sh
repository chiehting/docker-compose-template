#!/bin/bash

# 設定變數
POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_DB=${POSTGRES_DB:-keycloak}
POSTGRES_USER=${POSTGRES_USER:-keycloak}
BACKUP_DIR="/backups"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-14}
WEEKLY_RETENTION_DAYS=${WEEKLY_RETENTION_DAYS:-14}
ENCRYPTION_KEY=${BACKUP_ENCRYPTION_KEY}
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_TYPE=${1:-daily}
LOG_FILE="${BACKUP_DIR}/backup.log"

# 建立備份目錄
mkdir -p ${BACKUP_DIR}/{daily,weekly,monthly}

# 設定備份路徑
case $BACKUP_TYPE in
    "weekly")
        BACKUP_PATH="${BACKUP_DIR}/weekly"
        RETENTION=$WEEKLY_RETENTION_DAYS
        ;;
    "monthly")
        BACKUP_PATH="${BACKUP_DIR}/monthly"
        RETENTION=365
        ;;
    *)
        BACKUP_PATH="${BACKUP_DIR}/daily"
        RETENTION=$RETENTION_DAYS
        ;;
esac

BACKUP_FILE="${BACKUP_PATH}/keycloak_${BACKUP_TYPE}_${DATE}"

# 記錄開始時間
echo "[$(date)] Starting ${BACKUP_TYPE} backup..." >> ${LOG_FILE}

# 檢查資料庫連線
pg_isready -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB}
if [ $? -ne 0 ]; then
    echo "[$(date)] Database is not ready!" >> ${LOG_FILE}
    exit 1
fi

# 執行備份
pg_dump -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
    --verbose --clean --if-exists --create \
    --format=custom --compress=9 \
    --file=${BACKUP_FILE}.dump 2>> ${LOG_FILE}

# 檢查備份是否成功
if [ $? -eq 0 ]; then
    echo "[$(date)] Database dump completed successfully" >> ${LOG_FILE}
    
    # 建立純 SQL 備份
    pg_dump -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
        --verbose --clean --if-exists --create \
        --file=${BACKUP_FILE}.sql 2>> ${LOG_FILE}
    
    # 壓縮 SQL 備份
    gzip ${BACKUP_FILE}.sql
    
    # 如果設定了加密金鑰，進行加密
    if [ ! -z "$ENCRYPTION_KEY" ]; then
        echo "[$(date)] Encrypting backups..." >> ${LOG_FILE}
        
        # 加密 dump 文件
        gpg --batch --yes --passphrase="$ENCRYPTION_KEY" \
            --cipher-algo AES256 --compress-algo 2 \
            --symmetric --output ${BACKUP_FILE}.dump.gpg \
            ${BACKUP_FILE}.dump
        
        # 加密 SQL 文件
        gpg --batch --yes --passphrase="$ENCRYPTION_KEY" \
            --cipher-algo AES256 --compress-algo 2 \
            --symmetric --output ${BACKUP_FILE}.sql.gz.gpg \
            ${BACKUP_FILE}.sql.gz
        
        # 刪除未加密文件
        rm ${BACKUP_FILE}.dump ${BACKUP_FILE}.sql.gz
        
        echo "[$(date)] Encryption completed" >> ${LOG_FILE}
    fi
    
    # 建立備份資訊文件
    cat > ${BACKUP_FILE}.info << EOF
Backup Information
==================
Date: $(date)
Type: ${BACKUP_TYPE}
Database: ${POSTGRES_DB}
Host: ${POSTGRES_HOST}
User: ${POSTGRES_USER}
Encrypted: $([ ! -z "$ENCRYPTION_KEY" ] && echo "Yes" || echo "No")
Files:
$(ls -la ${BACKUP_PATH}/keycloak_${BACKUP_TYPE}_${DATE}.*)
EOF
    
    echo "[$(date)] Backup completed successfully" >> ${LOG_FILE}
else
    echo "[$(date)] Backup failed!" >> ${LOG_FILE}
    exit 1
fi

# 清理舊備份
echo "[$(date)] Cleaning up old ${BACKUP_TYPE} backups (older than ${RETENTION} days)..." >> ${LOG_FILE}
find ${BACKUP_PATH} -name "keycloak_${BACKUP_TYPE}_*" -mtime +${RETENTION} -delete

# 檢查磁碟空間
DISK_USAGE=$(df ${BACKUP_DIR} | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "[$(date)] WARNING: Backup disk usage is ${DISK_USAGE}%" >> ${LOG_FILE}
fi

# 記錄完成時間和統計
BACKUP_SIZE=$(du -sh ${BACKUP_PATH}/keycloak_${BACKUP_TYPE}_${DATE}.* 2>/dev/null | awk '{print $1}' | head -1)
echo "[$(date)] ${BACKUP_TYPE} backup process completed. Size: ${BACKUP_SIZE}" >> ${LOG_FILE}

# 保持日誌文件大小
tail -n 2000 ${LOG_FILE} > ${LOG_FILE}.tmp && mv ${LOG_FILE}.tmp ${LOG_FILE}

# 發送備份狀態到監控系統（可選）
if command -v curl &> /dev/null && [ ! -z "$HEALTHCHECK_URL" ]; then
    curl -fsS -m 10 --retry 5 -o /dev/null "$HEALTHCHECK_URL" || true
fi