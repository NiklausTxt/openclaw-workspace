#!/bin/bash

# 按日期分组建军照片的脚本
# 用途：根据照片的文件修改时间（近似拍摄时间）分组整理
# 作者：建国
# 创建时间：2026-03-03

set -e

# 配置
SOURCE_DIR="/Users/tongxiaotong/littleCat/pic"
OUTPUT_BASE="/Users/tongxiaotong/littleCat/pic_grouped"
WORKSPACE="/Users/tongxiaotong/.openclaw/workspace/jianjun"

# 创建输出目录
mkdir -p "$OUTPUT_BASE"

# 日志文件
LOG_FILE="$WORKSPACE/grouping.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== 开始按日期分组照片 ==="

# 统计总数
TOTAL=$(find "$SOURCE_DIR" -maxdepth 1 -type f \( -name "*.JPG" -o -name "*.jpg" -o -name "*.JPEG" -o -name "*.jpeg" \) | wc -l | tr -d ' ')
log "找到 $TOTAL 张照片"

# 按月分组
log "开始按月分组..."
for month in 2025-08 2025-09 2025-10 2025-11 2025-12 2026-01 2026-02 2026-03; do
    MONTH_DIR="$OUTPUT_BASE/$month"
    mkdir -p "$MONTH_DIR"

    # 查找该月的照片（通过stat的修改时间）
    COUNT=0
    for file in "$SOURCE_DIR"/*.{JPG,jpg,JPEG,jpeg}; do
        if [ -f "$file" ]; then
            # 获取文件修改时间的年月
            FILE_DATE=$(stat -f "%Sm" -t "%Y-%m" "$file" 2>/dev/null || echo "")
            if [ "$FILE_DATE" = "$month" ]; then
                # 按天进一步分组
                DAY=$(stat -f "%Sm" -t "%Y-%m-%d" "$file" 2>/dev/null || echo "")
                if [ -n "$DAY" ]; then
                    DAY_DIR="$MONTH_DIR/$DAY"
                    mkdir -p "$DAY_DIR"

                    # 复制文件（不移动，保持原文件）
                    cp "$file" "$DAY_DIR/"
                    COUNT=$((COUNT + 1))
                fi
            fi
        fi
    done

    if [ $COUNT -gt 0 ]; then
        log "✓ $month: $COUNT 张照片"
    fi
done

log "=== 分组完成 ==="
log "照片已按日期分组到: $OUTPUT_BASE"
