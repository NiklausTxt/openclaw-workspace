#!/bin/bash
# OpenClaw 任务管理系统快速测试脚本

set -e

MEMORY_DIR="/Users/tongxiaotong/.openclaw/workspace/memory"
TASKS_DIR="$MEMORY_DIR/tasks"
ACTIVE_DIR="$MEMORY_DIR/active"

echo "🚀 OpenClaw 任务管理系统测试"
echo ""

# 1. 检查目录结构
echo "📁 检查目录结构..."
for dir in "$TASKS_DIR" "$ACTIVE_DIR" "$MEMORY_DIR/raw-chat"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir (不存在)"
    fi
done
echo ""

# 2. 查看当前任务状态
echo "📊 当前任务状态:"
if [ -f "$ACTIVE_DIR/current-task.md" ]; then
    cat "$ACTIVE_DIR/current-task.md"
else
    echo "  current-task.md 不存在"
fi
echo ""

# 3. 列出所有任务
echo "📋 已创建任务:"
if [ -d "$TASKS_DIR" ]; then
    for task in "$TASKS_DIR"/*; do
        if [ -d "$task" ]; then
            task_name=$(basename "$task")
            if [ -f "$task/status.json" ]; then
                state=$(grep -o '"state":"[^"]*"' "$task/status.json" | cut -d'"' -f4)
                echo "  - $task_name (state: $state)"
            else
                echo "  - $task_name (无状态文件)"
            fi
        fi
    done
else
    echo "  无任务"
fi
echo ""

# 4. 查看变更日志
echo "📝 任务切换日志 (最近5条):"
if [ -f "$ACTIVE_DIR/change-log.md" ]; then
    tail -10 "$ACTIVE_DIR/change-log.md" | head -10
else
    echo "  change-log.md 不存在"
fi
echo ""

echo "✅ 测试完成！"
