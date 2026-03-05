# Task Scheduler - 统一任务调度器

任务调度器负责统一管理所有task的待办任务，每10分钟轮询一次，单次执行一个任务。

## 目录结构

```
.openclaw/workspace/
├── memory/
│   ├── scheduler_execution_log.md  # 全局执行流水表
│   └── scheduler_lock.json        # 调度器锁
├── tasks/
│   └── {task_name}/
│       └── todo_list.md           # 任务待办列表
```

## todo_list.md 格式

每个task的todo_list.md必须包含以下结构：

```markdown
# 待办任务列表

## 元数据

- task_name: trading_simulation
- version: 1.0
- last_updated: 2026-03-05T18:40:00+08:00

---

## 待办任务列表

| unique_key | task_name | description | due_time | priority | timeout | max_retries | next_execute_after | status | last_execution | locked_by | locked_at |
|------------|-----------|-------------|----------|----------|---------|-------------|-------------------|--------|----------------|-----------|-----------|
| trading_buy_check | 购买检查 | 检查市场并执行购买 | 2026-03-05T14:00:00+08:00 | high | 5 | 3 | - | pending | - | - | - |
| trading_daily_review | 每日复盘 | 生成每日交易复盘 | 2026-03-05T20:00:00+08:00 | normal | 10 | 2 | 1d | pending | - | - | - |

---

## 历史记录

| unique_key | status | execute_time | result | error_message |
|------------|--------|--------------|--------|---------------|
| trading_buy_check | completed | 2026-03-04T14:05:00+08:00 | success | - |

---

## 统计

- 总任务数：2
- 待执行：2
- 执行中：0
- 已完成：0
- 失败：0
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| unique_key | string | 是 | 任务唯一标识（全局唯一） |
| task_name | string | 是 | 任务名称（简短描述） |
| description | string | 是 | 任务详细描述 |
| due_time | ISO8601 | 是 | 计划执行时间 |
| priority | string | 否 | 优先级：high/normal/low（默认normal） |
| timeout | number | 否 | 超时时间（分钟，默认10） |
| max_retries | number | 否 | 最大重试次数（默认3） |
| next_execute_after | string | 否 | 周期性任务间隔（如1d、2h、30m） |
| status | string | 是 | 状态：pending/running/completed/failed/retry |
| last_execution | ISO8601 | 否 | 上次执行时间 |
| locked_by | string | 否 | 锁持有者（task_scheduler） |
| locked_at | ISO8601 | 否 | 锁定时间 |

## 调度器执行流程

### 1. 获取调度器锁

检查`scheduler_lock.json`，如果锁存在且未过期（<10分钟），跳过本次执行。

### 2. 扫描所有task的todo_list.md

遍历`tasks/`目录下所有task，读取每个task的`todo_list.md`。

### 3. 筛选可执行任务

筛选条件：
- `status` = `pending` 或 `retry`
- `due_time` ≤ 当前时间
- `locked_by` 为空或已过期（>5分钟）

排序规则：
1. 按`priority`排序（high > normal > low）
2. 按`due_time`排序（早的优先）

### 4. 执行第一个任务

- 更新`status`为`running`，设置锁
- 记录到流水表（开始时间）
- 执行任务逻辑
- 记录执行结果到流水表
- 更新todo_list.md的`status`和`last_execution`
- 如果成功且有`next_execute_after`，更新`due_time`

### 5. 释放调度器锁

删除或更新`scheduler_lock.json`

### 6. 返回

单次只执行一个任务，下次再轮询。

## 状态转换图

```
pending → running → completed
   ↓          ↓
retry ← failed
```

## 使用方法

### 手动触发

运行调度器执行一次：

```bash
openclaw skills run task-scheduler
```

### 配置定时任务

创建cron，每10分钟执行一次：

```bash
openclaw cron create "task-scheduler" "0 */10 * * * *" "openclaw skills run task-scheduler"
```

### 创建新任务的todo_list.md

在task目录下创建`todo_list.md`，参考上面的格式。

### 查看执行历史

查看全局流水表：

```bash
cat ~/.openclaw/workspace/memory/scheduler_execution_log.md
```

## 注意事项

1. **避免任务执行时间过长**：单个任务应该在10分钟内完成，否则会阻塞下次调度
2. **超时设置**：为任务设置合理的`timeout`，避免任务卡住
3. **重试机制**：失败的任务会自动重试，最多`max_retries`次
4. **周期性任务**：设置`next_execute_after`，任务完成后自动计算下次执行时间
5. **锁过期**：已锁任务如果超过5分钟未更新，自动解锁，下次可重新执行

## 任务执行示例

当调度器执行一个任务时，会调用task目录下的`execute.md`（如果存在）或根据任务类型执行相应操作。

例如，`trading_simulation`任务的执行逻辑应该写在`tasks/trading_simulation/execute.md`中。
