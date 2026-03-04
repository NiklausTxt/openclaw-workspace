# 飞书命令配置指南

## 概述

在飞书中配置自定义命令来管理 OpenClaw 任务系统，方便切换任务、更新上下文。

## 命令列表

### 1. 切换任务

**命令**: `/switch_task` 或 `/st`
**参数**: `[task_id]` (可选)
**描述**: 切换到指定任务，或创建新任务

**示例**:
- `/st jianjun-xiaohongshu` - 切换到建军小红书任务
- `/st` - 切换到原始聊天记录模式

**实现逻辑**:
```
1. 若 task_id 为空，自动创建 raw-chat-<date> 任务
2. 若 task_id 不存在，创建任务目录结构
3. 更新 /active/current-task.md
4. 记录切换日志到 /active/change-log.md
```

---

### 2. 更新任务

**命令**: `/update_task` 或 `/ut`
**参数**: 无
**描述**: 将当前聊天记录更新到任务文件中

**实现逻辑**:
```
1. 检查是否有活跃任务
2. 提取从 started_at 到现在的聊天内容
3. 语义分析分类：
   - 目标变化 → goal.md
   - 背景补充 → context.md
   - 决策结论 → decisions.md
   - 普通内容 → chat-log.md
4. 更新 status.json 时间戳
```

---

### 3. 关闭任务

**命令**: `/close_task` 或 `/ct`
**参数**: 无
**描述**: 完成当前任务并标记为已完成

**实现逻辑**:
```
1. 检查是否有活跃任务
2. 更新 status.json 为 completed
3. 清空 current-task.md
4. 记录到 change-log.md
```

---

### 4. 查看任务

**命令**: `/current_task` 或 `/ctask`
**参数**: 无
**描述**: 查看当前活跃任务的状态信息

**输出示例**:
```
task_id: demo-task
state: active
started_at: 2026-03-04T17:00:00Z
last_updated: 2026-03-04T17:00:00Z
```

---

## 在飞书开放平台配置命令

### 步骤 1: 创建机器人应用

1. 登录飞书开放平台
2. 创建新应用 → 选择"企业自建应用"
3. 获取 App ID 和 App Secret

### 步骤 2: 配置机器人权限

申请以下权限：
- `im:message` - 接收消息
- `im:message:send_as_bot` - 发送消息
- `im:chat` - 获取聊天信息

### 步骤 3: 配置自定义指令

在飞书开放平台 → 应用配置 → 指令管理中添加：

#### /switch_task 指令
```
指令名称: switch_task
指令描述: 切换或创建任务
指令参数: [task_id]
指令别名: st
```

#### /update_task 指令
```
指令名称: update_task
指令描述: 更新当前任务
指令参数: 无
指令别名: ut
```

#### /close_task 指令
```
指令名称: close_task
指令描述: 关闭当前任务
指令参数: 无
指令别名: ct
```

#### /current_task 指令
```
指令名称: current_task
指令描述: 查看当前任务
指令参数: 无
指令别名: ctask
```

### 步骤 4: 配置消息回调URL

设置回调URL指向你的 OpenClaw 服务地址：

```
https://your-openclaw-server.com/webhook/feishu
```

### 步骤 5: 发布应用

1. 提交应用审核
2. 审核通过后发布到工作台
3. 在飞书聊天中测试命令

---

## 本地测试

在飞书命令配置完成前，可以直接在 OpenClaw 中测试：

```bash
# 切换任务
# 直接调用相关函数或命令
# 例如：读取 /memory/tasks/demo-task/status.json
```

---

## 常见问题

### Q: 命令没反应？
A: 检查机器人权限是否已授权，回调URL是否正确。

### Q: task_id 怎么命名？
A: 建议使用 kebab-case，如 `jianjun-xiaohongshu`, `daily-notes`。

### Q: 如何查看所有任务？
A: 读取 `/memory/tasks/` 目录，列出所有子目录。

### Q: 任务可以暂停吗？
A: 可以，在 status.json 中将 state 设为 `paused`。

---

**创建时间**: 2026-03-04
**相关文件**: memory-manual.md
