# ✅ OpenClaw 记忆系统命令规范（V2 严谨版）

> 本规范仅定义命令行为，不描述实现细节。  
> 所有命令必须 **幂等、安全、可回溯**。

---

# 一、任务切换命令

## 1️⃣ 切换活跃任务

### 主命令

```
/switch_task <task_id>
```

### 缩写

```
/st <task_id>
```

---

## 行为规范

### 1. 参数规则

| 参数 | 必填 | 说明 |
|------|------|------|
| task_id | 否 | 若不存在则创建任务；若为空则自动关联 raw-chat |

---

### 2. 执行逻辑

#### 情况 A：指定 task_id

1. 若 `/memory/tasks/<task_id>` 不存在：
   - 自动创建目录结构：

   ```
   /memory/tasks/<task_id>/
       goal.md
       context.md
       chat-log.md
       decisions.md
       status.json
   ```

   - 初始化 status.json：

   ```json
   {
       "task_id": "<task_id>",
       "created_at": "<now>",
       "updated_at": "<now>",
       "state": "active",
       "version": 1
   }
   ```

2. 读取 `/active/current-task.md`
3. 记录原 task_id（若存在）
4. 更新 `/active/current-task.md`：

   ```json
   {
       "active": true,
       "task_id": "<task_id>",
       "started_at": "<now>"
   }
   ```

5. 在 `/active/change-log.md` 追加：

   ```
   ## <timestamp>
   from: <old_task_id | none>
   to: <task_id>
   reason: manual_switch
   ```

---

#### 情况 B：未指定 task_id

自动执行：

```
/st raw-chat-<latest-date>
```

执行逻辑：

1. 查找 `/memory/raw-chat/` 最新文件
2. 创建任务：

   ```
   task_id = raw-chat-YYYY-MM-DD
   ```

3. 后续流程同“情况 A”

---

# 二、任务更新命令

## 2️⃣ 更新当前活跃任务

### 主命令

```
/update_task
```

### 缩写

```
/ut
```

---

## 前置校验

1. 读取 `/active/current-task.md`
2. 若：

```
active != true
```

则报错：

```
ERROR: No active task. Use /switch_task first.
```

---

## 执行逻辑

### 1️⃣ 时间范围计算

```
start_time = current-task.started_at
end_time   = now
```

仅提取此时间段内的聊天记录。

---

### 2️⃣ 内容分类更新规则

系统根据语义分析，将新增聊天内容分流至：

| 类型 | 文件 | 更新方式 |
|------|------|----------|
| 任务目标变化 | goal.md | 追加新版本，不覆盖 |
| 背景补充 | context.md | 追加 |
| 决策结论 | decisions.md | 追加决策条目 |
| 普通过程记录 | chat-log.md | 全量追加 |
| 状态变更 | status.json | 更新 state + updated_at |

---

### 3️⃣ 更新格式规范

#### goal.md 追加格式

```
## Update @ <timestamp>
<summary>
```

---

#### decisions.md 追加格式

```
## Decision @ <timestamp>
- Context:
- Decision:
- Impact:
```

---

#### chat-log.md 追加格式

```
## Log @ <timestamp>
<raw extracted chat>
```

---

#### status.json 更新规范

仅允许修改：

```json
{
    "updated_at": "<now>",
    "state": "active | paused | completed"
}
```

禁止删除字段。

---

### 4️⃣ 更新完成后

自动刷新：

```
current-task.started_at = now
```

确保下次 `/ut` 不重复扫描。

---

# 三、任务关闭命令（新增）

## 3️⃣ 关闭当前任务

### 主命令

```
/close_task
```

### 缩写

```
/ct
```

---

## 行为

1. 校验 active = true
2. 更新：

`/memory/tasks/<task_id>/status.json`

```json
{
    "state": "completed",
    "updated_at": "<now>"
}
```

3. 更新 `/active/current-task.md`

```json
{
    "active": false,
    "task_id": null,
    "started_at": null
}
```

4. change-log.md 追加：

```
## <timestamp>
from: <task_id>
to: none
reason: completed
```

---

# 四、任务状态查看命令（新增）

## 4️⃣ 查看当前任务

```
/current_task
```

缩写：

```
/ctask
```

输出：

```
task_id:
state:
started_at:
last_updated:
```

数据来源：

- current-task.md
- tasks/<task_id>/status.json

---

# 五、安全约束规则（强制）

1. 所有 JSON 文件必须合法 JSON
2. 所有时间格式统一：

```
ISO8601 UTC
YYYY-MM-DDTHH:MM:SSZ
```

3. 所有命令必须幂等：
   - 重复执行不得破坏数据
4. 不允许覆盖已有内容
5. 所有追加必须带时间戳
6. change-log 不可修改历史记录

---

# 六、命令总览

| 命令 | 作用 |
|------|------|
| `/switch_task <task_id>` | 切换或创建任务 |
| `/st <task_id>` | 简写 |
| `/update_task` | 更新任务内容 |
| `/ut` | 简写 |
| `/close_task` | 关闭任务 |
| `/ct` | 简写 |
| `/current_task` | 查看当前任务 |
| `/ctask` | 简写 |

---

✅ 本版本特性：

- 严格状态机设计
- 时间窗口增量更新
- 强制版本可追溯
- 幂等安全
- 自动创建任务
- 支持 raw-chat 自动归档
- 增加任务关闭机制
- 增加任务查询机制

---

可直接交付 OpenClaw 实现。