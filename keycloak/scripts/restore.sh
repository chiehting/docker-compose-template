#!/bin/bash

# 使用方法: ./restore.sh <backup_file> [--force]

POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_DB=${POSTGRES_DB:-keycloak}
POSTGRES_USER=${POSTGRES_USER:-keycloak}
BACKUP_DIR="/backups"
ENCRYPTION_KEY=${BACKUP_ENCRYPTION_KEY}
LOG_FILE="${BACKUP_DIR}/restore.log"
FORCE_RESTORE=${2:-false}

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file> [--force]"
    echo "Available backups:"
    find ${BACKUP_DIR} -name "*.dump*" -o -name "*.sql.gz*" | sort
    exit 1
fi

BACKUP_FILE="$1"

# 檢查備份文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "[$(date)] Starting restore from: $BACKUP_FILE" >> ${LOG_FILE}

# 如果是加密文件，先解密
if [[ "$BACKUP_FILE" == *.gpg ]]; then
    if [ -z "$ENCRYPTION_KEY" ]; then
        echo "Encrypted backup requires BACKUP_ENCRYPTION_KEY environment variable"
        exit 1
    fi
    
    DECRYPTED_FILE="${BACKUP_FILE%.gpg}"
    echo "[$(date)] Decrypting backup file..." >> ${LOG_FILE}
    
    gpg --batch --yes --passphrase="$ENCRYPTION_KEY" \
        --decrypt --output "$DECRYPTED_FILE" "$BACKUP_FILE"
    
    if [ $? -ne 0 ]; then
        echo "[$(date)] Decryption failed!" >> ${LOG_FILE}
        exit 1
    fi
    
    BACKUP_FILE="$DECRYPTED_FILE"
    CLEANUP_DECRYPTED=true
fi

# 確認恢復操作
if [ "$FORCE_RESTORE" != "--force" ]; then
    echo "WARNING: This will completely replace the current database!"
    echo "Current database: $POSTGRES_DB on $POSTGRES_HOST"
    echo "Backup file: $BACKUP_FILE"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Restore cancelled."
        exit 0
    fi
fi

# 檢查資料庫連線
pg_isready -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d postgres
if [ $? -ne 0 ]; then
    echo "[$(date)] Database server is not ready!" >> ${LOG_FILE}
    exit 1
fi

# 建立恢復前備份
echo "[$(date)] Creating pre-restore backup..." >> ${LOG_FILE}
PRE_RESTORE_BACKUP="${BACKUP_DIR}/pre_restore_$(date +%Y%m%d_%H%M%S).dump"
pg_dump -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
    --format=custom --compress=9 \
    --file="$PRE_RESTORE_BACKUP" 2>> ${LOG_FILE}

# 執行恢復
echo "[$(date)] Starting database restore..." >> ${LOG_FILE}

if [[ "$BACKUP_FILE" == *.dump ]]; then
    # Custom format restore
    pg_restore -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d postgres \
        --clean --if-exists --create --verbose \
        "$BACKUP_FILE" 2>> ${LOG_FILE}
elif [[ "$BACKUP_FILE" == *.sql.gz ]]; then
    # SQL format restore
    gunzip -c "$BACKUP_FILE" | psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d postgres \
        2>> ${LOG_FILE}
elif [[ "$BACKUP_FILE" == *.sql ]]; then
    # Plain SQL restore
    psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d postgres \
        -f "$BACKUP_FILE" 2>> ${LOG_FILE}
else
    echo "[$(date)] Unsupported backup file format!" >> ${LOG_FILE}
    exit 1
fi

# 檢查恢復結果
if [ $? -eq 0 ]; then
    echo "[$(date)] Database restore completed successfully" >> ${LOG_FILE}
    
    # 驗證恢復
    TABLE_COUNT=$(psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
        -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null)
    
    echo "[$(date)] Restored database contains $TABLE_COUNT tables" >> ${LOG_FILE}
    
    # 清理解密文件
    if [ "$CLEANUP_DECRYPTED" = true ]; then
        rm -f "$DECRYPTED_FILE"
    fi
    
    echo "Restore completed successfully!"
    echo "Pre-restore backup saved as: $PRE_RESTORE_BACKUP"
else
    echo "[$(date)] Database restore failed!" >> ${LOG_FILE}
    echo "Restore failed! Check log file: $LOG_FILE"
    exit 1
fi