# 记忆文件系统 (V2 任务管理系统)

## 目录结构

```
memory/
├── YYYY-MM-DD.md              # 每日记忆（重要事件、操作记录）
├── tasks/                    # 任务目录
│   └── <task_id>/           # 具体任务
│       ├── goal.md           # 任务目标
│       ├── context.md        # 任务背景
│       ├── chat-log.md       # 聊天日志
│       ├── decisions.md      # 决策记录
│       └── status.json       # 任务状态
├── active/                   # 活跃任务状态
│   ├── current-task.md      # 当前任务信息（JSON）
│   └── change-log.md        # 任务切换日志
├── projects/                # 项目相关记录
│   ├── INDEX.md
│   ├── jianjun-xiaohongshu/
│   └── daily-life/
└── archive/                 # 归档记录
```

## 任务管理系统命令

### 切换任务
```
/switch_task <task_id>  或 /st <task_id>
```
- 指定 task_id：切换到该任务（不存在则创建）
- 不指定 task_id：切换到当前激活的任务（无操作）

### 更新任务
```
/update_task 或 /ut
```
- 根据聊天记录更新当前任务
- 自动分类内容到对应文件

### 关闭任务
```
/close_task 或 /ct
```
- 标记当前任务为 completed
- 清空活跃任务状态

### 查看当前任务
```
/current_task 或 /ctask
```
- 显示当前活跃任务信息

## 文件规范

### status.json 格式
```json
{
    "task_id": "任务ID",
    "created_at": "ISO8601时间",
    "updated_at": "ISO8601时间",
    "state": "active|paused|completed",
    "version": 版本号
}
```

### current-task.md 格式
```json
{
    "active": true|false,
    "task_id": "任务ID或null",
    "started_at": "ISO8601时间或null"
}
```

### 更新时间戳格式
统一使用 ISO8601 UTC: `YYYY-MM-DDTHH:MM:SSZ`

## 安全约束

- 所有 JSON 文件必须合法
- 不允许覆盖已有内容
- 所有追加必须带时间戳
- 命令必须幂等

---

**创建时间**: 2026-03-04
**版本**: V2.0
**规范来源**: memory-manual.md
