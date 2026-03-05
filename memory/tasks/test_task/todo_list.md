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
|test_repeat|周期性测试|每10分钟执行一次|2026-03-06 03:10:55|normal|5|3|10m|pending|2026-03-06 03:00:55|-|-|

---

## 历史记录

| unique_key | status | execute_time | result | error_message |
|------------|--------|--------------|--------|---------------|
| test_repeat | completed | 2026-03-06 03:00:55 | success | - |
| test_repeat | completed | 2026-03-06 02:40:53 | success | - |
| test_repeat | completed | 2026-03-06 02:30:06 | success | - |
| test_repeat | completed | 2026-03-05 23:11:24 | success | - |
| test_repeat | completed | 2026-03-05T14:50:40.902125+00:00 | success | - |
| test_repeat | completed | 2026-03-05T14:30:53.140463+00:00 | success | - |
| test_repeat | completed | 2026-03-05T14:10:41.175636+00:00 | success | - |
| test_repeat | completed | 2026-03-05T13:50:39.917259+00:00 | success | - |
| test_repeat | completed | 2026-03-05T13:31:21.624466+00:00 | success | - |
| test_repeat | completed | 2026-03-05T13:20:38.165910+00:00 | success | - |
| test_repeat | completed | 2026-03-05T13:00:55.815227+00:00 | success | - |
| test_repeat | completed | 2026-03-05T12:40:43.650189+00:00 | success | - |
| test_repeat | completed | 2026-03-05T12:30:34.402060+00:00 | success | - |
| test_repeat | completed | 2026-03-05T12:10:45.543247+00:00 | success | - |
| test_repeat | completed | 2026-03-05T11:50:37.786863+00:00 | success | - |
| test_repeat | completed | 2026-03-05T11:40:34.827714+00:00 | success | - |
| test_repeat | completed | 2026-03-05T11:30:32.162435+00:00 | success | - |
| test_repeat | completed | 2026-03-05T11:10:42.517502+00:00 | success | - |
| test_repeat | completed | 2026-03-05T11:00:29.577618+00:00 | success | - |
| test_repeat | completed | 2026-03-05T10:46:25.655329+00:00 | success | - |

---

## 统计

- 总任务数：2
- 待执行：2
- 执行中：0
- 已完成：0
- 失败：0
