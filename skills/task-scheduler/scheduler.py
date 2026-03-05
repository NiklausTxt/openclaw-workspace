#!/usr/bin/env python3
"""
任务调度器 - 统一管理所有task的待办任务
每10分钟轮询一次，单次执行一个任务
"""

import os
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
import re

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
TASKS_DIR = MEMORY_DIR / "tasks"
EXECUTION_LOG = MEMORY_DIR / "scheduler_execution_log.md"
LOCK_FILE = MEMORY_DIR / "scheduler_lock.json"
LOCK_EXPIRE_MINUTES = 10  # 调度器锁过期时间
TASK_LOCK_EXPIRE_MINUTES = 5  # 任务锁过期时间

# 优先级映射
PRIORITY_MAP = {"high": 0, "normal": 1, "low": 2}


def read_file(path):
    """读取文件内容"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败: {path}, 错误: {e}")
        return None


def write_file(path, content):
    """写入文件内容"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 写入文件失败: {path}, 错误: {e}")
        return False


def parse_iso8601(time_str):
    """解析ISO8601格式时间"""
    if not time_str or time_str == "-":
        return None
    try:
        return datetime.fromisoformat(time_str)
    except:
        return None


def format_iso8601(dt):
    """格式化为 日期+时间格式 (YYYY-MM-DD HH:MM:SS)"""
    if dt is None:
        return "-"
    # 转换为GMT+8时区的时间字符串
    return (dt + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def get_scheduler_lock():
    """获取调度器锁"""
    if not LOCK_FILE.exists():
        return None

    try:
        with open(LOCK_FILE, "r", encoding="utf-8") as f:
            lock_data = json.load(f)
    except:
        return None

    if not lock_data:
        return None

    locked_at = parse_iso8601(lock_data.get("locked_at"))
    if locked_at is None:
        return None

    # 检查锁是否过期
    if datetime.now(timezone.utc) - locked_at > timedelta(minutes=LOCK_EXPIRE_MINUTES):
        return None

    return lock_data


def acquire_scheduler_lock():
    """获取调度器锁"""
    now = datetime.now(timezone.utc)
    lock_data = {
        "locked_by": "task_scheduler",
        "locked_at": format_iso8601(now)
    }

    if write_file(LOCK_FILE, json.dumps(lock_data, indent=2, ensure_ascii=False)):
        return lock_data
    return None


def release_scheduler_lock():
    """释放调度器锁"""
    write_file(LOCK_FILE, "{}")


def parse_todo_list(todo_path):
    """解析todo_list.md文件"""
    content = read_file(todo_path)
    if not content:
        return None

    tasks = []
    lines = content.split("\n")

    # 找到表格开始位置（待办任务列表）
    table_start = None
    for i, line in enumerate(lines):
        if "unique_key" in line and "due_time" in line:
            table_start = i + 2  # 跳过表头和分隔线
            break

    if table_start is None:
        return []

    # 解析表格行
    for line in lines[table_start:]:
        if not line.strip() or not line.startswith("|"):
            if line.strip().startswith("---"):
                continue
            break  # 表格结束

        # 解析表格行
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 9:
            continue

        task = {
            "unique_key": parts[0],
            "task_name": parts[1],
            "description": parts[2],
            "due_time": parse_iso8601(parts[3]),
            "priority": parts[4] if parts[4] != "-" else "normal",
            "timeout": int(parts[5]) if parts[5] != "-" else 10,
            "max_retries": int(parts[6]) if parts[6] != "-" else 3,
            "next_execute_after": parts[7] if parts[7] != "-" else None,
            "status": parts[8],
            "last_execution": parse_iso8601(parts[9]) if parts[9] != "-" else None,
            "locked_by": parts[10] if parts[10] != "-" else None,
            "locked_at": parse_iso8601(parts[11]) if len(parts) > 11 and parts[11] != "-" else None
        }

        tasks.append(task)

    return tasks


def scan_all_tasks():
    """扫描所有task的todo_list.md"""
    all_tasks = []
    task_dirs = []

    if not TASKS_DIR.exists():
        return []

    for task_dir in TASKS_DIR.iterdir():
        if not task_dir.is_dir():
            continue

        todo_path = task_dir / "todo_list.md"
        if not todo_path.exists():
            continue

        tasks = parse_todo_list(todo_path)
        if tasks:
            for task in tasks:
                task["task_path"] = task_dir
                task["todo_path"] = todo_path
                all_tasks.append(task)

    return all_tasks


def filter_executable_tasks(tasks):
    """筛选可执行的任务"""
    now = datetime.now(timezone.utc)
    executable = []

    for task in tasks:
        # 状态检查
        if task["status"] not in ["pending", "retry"]:
            continue

        # 时间检查
        if task["due_time"] is None:
            continue
        if task["due_time"] > now:
            continue

        # 锁检查
        locked_by = task.get("locked_by")
        locked_at = task.get("locked_at")

        if locked_by:
            if locked_at and (now - locked_at) > timedelta(minutes=TASK_LOCK_EXPIRE_MINUTES):
                # 锁已过期，可以执行
                pass
            else:
                # 锁有效，跳过
                continue

        executable.append(task)

    # 排序：优先级 -> 时间
    executable.sort(key=lambda t: (
        PRIORITY_MAP.get(t["priority"], 1),
        t["due_time"]
    ))

    return executable


def update_task_status(task, status, error_message=None):
    """更新任务状态"""
    content = read_file(task["todo_path"])
    if not content:
        return False

    lines = content.split("\n")
    now = datetime.now(timezone.utc)

    # 找到任务行并更新
    table_start = None
    for i, line in enumerate(lines):
        if "unique_key" in line and "due_time" in line:
            table_start = i + 2
            break

    if table_start is None:
        return False

    for i in range(table_start, len(lines)):
        line = lines[i]
        if not line.strip() or not line.startswith("|"):
            break

        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 12:
            continue

        if parts[0] == task["unique_key"]:
            # 更新状态
            new_parts = parts.copy()
            new_parts[8] = status  # status
            new_parts[9] = format_iso8601(now)  # last_execution

            if status == "running":
                new_parts[10] = "task_scheduler"  # locked_by
                new_parts[11] = format_iso8601(now)  # locked_at
            else:
                new_parts[10] = "-"
                new_parts[11] = "-"

            lines[i] = "|" + "|".join(new_parts) + "|"
            break

    return write_file(task["todo_path"], "\n".join(lines))


def add_execution_log(task, status, duration, result, error_message=None):
    """添加执行记录到流水表"""
    content = read_file(EXECUTION_LOG)
    if not content:
        return False

    lines = content.split("\n")
    now = datetime.now(timezone.utc)

    # 找到表格位置
    table_start = None
    for i, line in enumerate(lines):
        if "execute_time" in line and "unique_key" in line:
            table_start = i + 2
            break

    if table_start is None:
        return False

    # 插入新记录
    new_line = f"| {format_iso8601(now)} | {task['unique_key']} | {task['task_name']} | {task['description']} | {status} | {duration}m | {result} | {error_message or '-'} |"

    lines.insert(table_start, new_line)

    # 更新元数据
    for i, line in enumerate(lines):
        if "last_scan_time:" in line:
            lines[i] = f"- last_scan_time: {format_iso8601(now)}"
        if "last_execution_time:" in line:
            lines[i] = f"- last_execution_time: {format_iso8601(now)}"

    return write_file(EXECUTION_LOG, "\n".join(lines))


def execute_task(task):
    """执行任务"""
    start_time = datetime.now(timezone.utc)

    # 更新状态为running
    if not update_task_status(task, "running"):
        return False, "更新任务状态失败"

    # 这里应该调用任务的执行逻辑
    # 暂时只是模拟执行
    print(f"🚀 执行任务: {task['unique_key']}")
    print(f"   描述: {task['description']}")
    print(f"   优先级: {task['priority']}")

    # 尝试找到任务的执行脚本
    execute_path = task["task_path"] / "execute.md"
    if execute_path.exists():
        print(f"   执行脚本: {execute_path}")
        # TODO: 实际执行任务逻辑
        # 这里可以调用openclaw来执行任务

    # 模拟执行
    import time
    time.sleep(1)  # 模拟任务执行

    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds() / 60

    # 标记为完成
    result = "success"
    error_message = None

    if not update_task_status(task, "completed"):
        result = "failed"
        error_message = "更新任务状态失败"

    # 添加执行记录
    add_execution_log(task, "completed", duration, result, error_message)

    return True, result


def calculate_next_execution(task):
    """计算下次执行时间"""
    if not task["next_execute_after"]:
        return None

    now = datetime.now(timezone.utc)
    interval_str = task["next_execute_after"]

    # 解析间隔
    if interval_str.endswith("m"):
        minutes = int(interval_str[:-1])
        return now + timedelta(minutes=minutes)
    elif interval_str.endswith("h"):
        hours = int(interval_str[:-1])
        return now + timedelta(hours=hours)
    elif interval_str.endswith("d"):
        days = int(interval_str[:-1])
        return now + timedelta(days=days)

    return None


def update_next_execution(task):
    """更新任务的下次执行时间"""
    next_time = calculate_next_execution(task)
    if next_time is None:
        return True

    content = read_file(task["todo_path"])
    if not content:
        return False

    lines = content.split("\n")

    # 找到任务行并更新due_time
    table_start = None
    for i, line in enumerate(lines):
        if "unique_key" in line and "due_time" in line:
            table_start = i + 2
            break

    if table_start is None:
        return False

    for i in range(table_start, len(lines)):
        line = lines[i]
        if not line.strip() or not line.startswith("|"):
            break

        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 12:
            continue

        if parts[0] == task["unique_key"]:
            # 重置状态为pending，更新due_time
            new_parts = parts.copy()
            new_parts[3] = format_iso8601(next_time)  # due_time
            new_parts[8] = "pending"  # status
            new_parts[10] = "-"
            new_parts[11] = "-"

            lines[i] = "|" + "|".join(new_parts) + "|"

            # 添加到历史记录
            history_start = None
            for j, line in enumerate(lines):
                if "unique_key" in line and "execute_time" in line and "status" in line:
                    history_start = j + 2
                    break

            if history_start:
                history_line = f"| {task['unique_key']} | completed | {format_iso8601(datetime.now(timezone.utc))} | success | - |"
                lines.insert(history_start, history_line)

            break

    return write_file(task["todo_path"], "\n".join(lines))


def main():
    """主函数"""
    print(f"🕒 任务调度器启动: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # 1. 检查调度器锁
    existing_lock = get_scheduler_lock()
    if existing_lock:
        print(f"⏰ 调度器已锁定，跳过本次执行")
        print(f"   锁定时间: {existing_lock.get('locked_at')}")
        print(f"   锁定者: {existing_lock.get('locked_by')}")
        return 0

    # 2. 获取调度器锁
    lock = acquire_scheduler_lock()
    if not lock:
        print("❌ 获取调度器锁失败")
        return 1

    print(f"✅ 获取调度器锁成功")

    try:
        # 3. 扫描所有task
        print(f"📂 扫描任务目录: {TASKS_DIR}")
        all_tasks = scan_all_tasks()
        print(f"   找到 {len(all_tasks)} 个待办任务")

        if not all_tasks:
            print("ℹ️  没有待办任务，跳过")
            return 0

        # 4. 筛选可执行任务
        executable_tasks = filter_executable_tasks(all_tasks)
        print(f"   可执行任务: {len(executable_tasks)} 个")

        if not executable_tasks:
            print("ℹ️  没有可执行的任务，跳过")
            return 0

        # 5. 执行第一个任务
        task = executable_tasks[0]
        print(f"🎯 准备执行任务: {task['unique_key']}")
        print(f"   描述: {task['description']}")
        print(f"   优先级: {task['priority']}")
        print(f"   计划时间: {format_iso8601(task['due_time'])}")

        success, result = execute_task(task)

        if success:
            print(f"✅ 任务执行成功: {result}")

            # 更新下次执行时间
            if task["next_execute_after"]:
                if update_next_execution(task):
                    next_time = calculate_next_execution(task)
                    print(f"📅 下次执行时间: {format_iso8601(next_time)}")
        else:
            print(f"❌ 任务执行失败: {result}")

    finally:
        # 6. 释放调度器锁
        release_scheduler_lock()
        print(f"🔓 释放调度器锁")

    print(f"✨ 调度器执行完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
