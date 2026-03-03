#!/bin/bash

# 建军照片相册自动监控脚本
# 用途：定期检测"建军"共享相册是否有新照片
# 作者：建国
# 创建时间：2026-03-03

set -e

# 配置
WORKSPACE="/Users/tongxiaotong/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/jianjun/auto_sync"
STATE_FILE="$SCRIPT_DIR/album_state.json"
SCREENSHOT_PATH="$SCRIPT_DIR/album_screenshot.png"
LOG_FILE="$SCRIPT_DIR/monitor.log"

# 创建日志目录
mkdir -p "$SCRIPT_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== 开始监控建军相册 ==="

# 步骤1：检查照片应用是否打开
log "检查照片应用状态..."
if ! pgrep -q "Photos"; then
    log "⚠️  照片应用未打开，尝试打开..."
    open -a "Photos"
    sleep 3
fi

# 步骤2：截图
log "截图照片应用..."
if command -v peekaboo &> /dev/null; then
    peekaboo image --app "照片" --window-index 0 --path "$SCREENSHOT_PATH" > /dev/null 2>&1
    if [ -f "$SCREENSHOT_PATH" ]; then
        log "✓ 截图成功: $SCREENSHOT_PATH"
    else
        log "✗ 截图失败"
        exit 1
    fi
else
    log "✗ peekaboo 未安装"
    exit 1
fi

# 步骤3：读取状态
log "读取状态文件..."
if [ -f "$STATE_FILE" ]; then
    LAST_COUNT=$(cat "$STATE_FILE" | grep -o '"last_photo_count":[0-9]*' | grep -o '[0-9]*')
    log "上次照片数量: $LAST_COUNT"
else
    LAST_COUNT=0
    log "状态文件不存在，初始化..."
fi

# 步骤4：AI 识别照片数量（这里需要调用 OpenClaw 的 AI 能力）
# 由于这个脚本是通过 cron 调用的，无法直接调用 OpenClaw 工具
# 所以这里只是框架，实际需要通过 OpenClaw 的 session 来处理

log "需要通过 OpenClaw session 分析截图并识别照片数量"
log "截图已保存，等待 AI 分析..."

# 输出结果，供 OpenClaw session 读取
echo "SCREENSHOT_PATH=$SCREENSHOT_PATH"
echo "LAST_COUNT=$LAST_COUNT"

log "=== 监控完成 ==="
