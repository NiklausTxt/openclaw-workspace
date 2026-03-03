#!/bin/bash

# 处理建军相册新照片的脚本
# 用途：分析新照片、提取元数据、准备小红书素材
# 作者：建国
# 创建时间：2026-03-03

set -e

# 配置
WORKSPACE="/Users/tongxiaotong/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/jianjun/auto_sync"
STATE_FILE="$SCRIPT_DIR/album_state.json"
METADATA_FILE="$WORKSPACE/jianjun/photos_metadata.json"
PHOTOS_WORKING_DIR="$WORKSPACE/jianjun/jianjun_photos"
LOG_FILE="$SCRIPT_DIR/process.log"

# 创建必要目录
mkdir -p "$SCRIPT_DIR"
mkdir -p "$PHOTOS_WORKING_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== 开始处理建军相册新照片 ==="

# 参数
PREVIOUS_COUNT=$1
CURRENT_COUNT=$2

if [ -z "$CURRENT_COUNT" ]; then
    log "错误: 缺少当前照片数量参数"
    exit 1
fi

# 计算新增照片数量
NEW_COUNT=$((CURRENT_COUNT - PREVIOUS_COUNT))

if [ $NEW_COUNT -le 0 ]; then
    log "没有新照片 (上次: $PREVIOUS_COUNT, 当前: $CURRENT_COUNT)"
    exit 0
fi

log "发现 $NEW_COUNT 张新照片！"
log "上次: $PREVIOUS_COUNT -> 当前: $CURRENT_COUNT"

# 这里应该有：
# 1. 通过 AppleScript 或快捷指令导出新照片
# 2. 分析照片内容
# 3. 提取元数据
# 4. 准备小红书素材

# 由于自动导出功能需要进一步探索，这里先记录发现
log "✓ 已检测到 $NEW_COUNT 张新照片"
log "✓ 等待人工确认导出或自动导出方案就绪"

# 更新状态
log "=== 处理完成 ==="

# 返回结果供调用者使用
echo "NEW_COUNT=$NEW_COUNT"
echo "PREVIOUS_COUNT=$PREVIOUS_COUNT"
echo "CURRENT_COUNT=$CURRENT_COUNT"
