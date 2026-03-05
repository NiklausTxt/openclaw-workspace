# 飞书命令配置指南

## 概述

在飞书中配置自定义命令来管理 OpenClaw 任务系统，方便切换任务、更新上下文。

## 命令列表

### 1. 切换任务

**命令**: `/switch_task` 或 `/st`
**参数**: `[task_id]` (可选)
**描述**: 切换到指定任务

**示例**:
- `/st jianjun-xiaohongshu` - 切换到建军小红书任务
- `/st trading_simulation` - 切换到交易模拟任务
- `/st` - 无操作，保持当前任务

**实现逻辑**:
```
1. 若 task_id 为空，无操作（保持当前任务）
2. 若 task_id 不存在，创建任务目录结构
3. 更新 /memory/active/current-task.md
4. 记录切换日志到 /memory/active/change-log.md
5. 若新创建任务，初始化基础文件：
   - goal.md, context.md, chat-log.md, decisions.md, status.json
```

---

### 2. 更新任务

**命令**: `/update_task` 或 `/ut`
**参数**: 无
**描述**: 将当前聊天记录更新到任务文件中

**实现逻辑**:
```
1. 读取 /memory/active/current-task.md
2. 若无活跃任务，报错："无活跃任务，请先使用 /switch_task 切换任务"
3. 提取从 started_at 到现在的聊天内容
4. 语义分析分类并追加到对应文件：
   - 目标变化 → goal.md (追加新版本)
   - 背景补充 → context.md (追加)
   - 决策结论 → decisions.md (追加决策条目)
   - 普通内容 → chat-log.md (追加)
5. 更新 status.json 的时间戳
6. 刷新 current-task.md 的 started_at
```

---

### 3. 关闭任务

**命令**: `/close_task` 或 `/ct`
**参数**: 无
**描述**: 完成当前任务并标记为已完成

**实现逻辑**:
```
1. 读取 /memory/active/current-task.md
2. 若无活跃任务，报错："无活跃任务"
3. 更新 /memory/tasks/<task_id>/status.json:
   - state: "completed"
   - updated_at: <now>
4. 清空 /memory/active/current-task.md:
   - active: false
   - task_id: null
   - started_at: null
5. 在 /memory/active/change-log.md 追加切换日志
```

---

### 4. 查看任务

**命令**: `/current_task` 或 `/ctask`
**参数**: 无
**描述**: 查看当前活跃任务的状态信息

**输出示例**:
```
task_id: trading_simulation
state: active
started_at: 2026-03-05T10:31:00Z
last_updated: 2026-03-05T15:00:00Z
```

**数据来源**:
- /memory/active/current-task.md
- /memory/tasks/<task_id>/status.json

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
# 切换任务（手动实现）
echo '{"task_id": "trading_simulation", "started_at": "2026-03-05T10:31:00Z"}' > /memory/active/current-task.md

# 更新任务（手动实现）
# 读取当前任务，分析聊天内容，更新对应文件

# 关闭任务（手动实现）
# 更新 status.json 为 completed，清空 current-task.md
```

---

## 常见问题

### Q: 命令没反应？
A: 检查机器人权限是否已授权，回调URL是否正确。

### Q: task_id 怎么命名？
A: 建议使用 kebab-case，如 `jianjun-xiaohongshu`, `trading_simulation`。

### Q: 如何查看所有任务？
A: 读取 `/memory/tasks/` 目录，列出所有子目录。

### Q: 任务可以暂停吗？
A: 可以，在 status.json 中将 state 设为 `paused`。

### Q: chat-log.md 和 daily memory 会重复吗？
A: 可能会，但这是设计如此：
- chat-log.md: 记录任务相关的聊天内容（任务特定）
- daily memory (memory/YYYY-MM-DD.md): 记录每日重要事件（全局）
- 如果没有活跃任务，不会产生 chat-log.md 的重复

---

**创建时间**: 2026-03-05
**相关文件**: memory/README.md, AGENTS.md
