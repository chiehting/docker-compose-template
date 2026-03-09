#!/bin/bash

# TDengine 健康檢查腳本
NODES=("tdengine-node1" "tdengine-node2" "tdengine-node3")

echo "TDengine 集群健康檢查 - $(date)"
echo "=================================="

for node in "${NODES[@]}"; do
    echo "檢查 $node..."
    
    # 檢查容器狀態
    if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$node.*Up"; then
        echo "  ✓ 容器運行正常"
        
        # 檢查 TDengine 服務
        if docker exec "$node" taos -s "show dnodes;" >/dev/null 2>&1; then
            echo "  ✓ TDengine 服務正常"
        else
            echo "  ✗ TDengine 服務異常"
        fi
    else
        echo "  ✗ 容器未運行"
    fi
    echo
done

# 檢查集群狀態
echo "集群狀態:"
docker exec tdengine-node1 taos -s "show dnodes;" 2>/dev/null || echo "無法獲取集群狀態"