# 待办任务列表

## 元数据

- task_name: test_task
- version: 1.0
- last_updated: 2026-03-05T18:50:00+08:00

---

## 待办任务列表

| unique_key | task_name | description | due_time | priority | timeout | max_retries | next_execute_after | status | last_execution | locked_by | locked_at |
|------------|-----------|-------------|----------|----------|---------|-------------|-------------------|--------|----------------|-----------|-----------|
|test_hello|测试任务|这是一个测试任务|2026-03-05T18:45:00+08:00|normal|5|3|-|completed|2026-03-05T10:46:12.447222+00:00|-|-|
|test_repeat|周期性测试|每10分钟执行一次|2026-03-05T10:56:25.655225+00:00|normal|5|3|10m|pending|2026-03-05T10:46:25.654221+00:00|-|-|

---

## 历史记录

| unique_key | status | execute_time | result | error_message |
|------------|--------|--------------|--------|---------------|
| test_repeat | completed | 2026-03-05T10:46:25.655329+00:00 | success | - |

---

## 统计

- 总任务数：2
- 待执行：2
- 执行中：0
- 已完成：0
- 失败：0
