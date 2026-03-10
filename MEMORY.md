# MEMORY.md - 长期记忆

## 记忆系统 (V2 任务管理)

当前使用任务化记忆管理系统，详见 [memory/README.md](memory/README.md)。

---

## 快速链接

- **记忆系统说明**: [memory/README.md](memory/README.md)
- **飞书命令配置**: [FEISHU_COMMANDS_SETUP.md](FEISHU_COMMANDS_SETUP.md)
- **任务管理规范**: [memory-manual.md](memory-manual.md)

---

## 永久记忆内容

### 模型切换策略（GLM 定价优化）

**规则**：
- **高峰期** (14:00-18:00 UTC+8): 使用 `zai/glm-4.7`（省额度，2x 消耗）
- **非高峰期**: 使用 `zai/glm-5`（旗舰模型，2x 消耗）

**原理**: GLM-5 高峰期 3x、非高峰期 2x 消耗；GLM-4.7 更便宜。高峰期用 4.7 省钱，其他时间用 5 获得更好效果。

**执行**: 每次会话开始时检查当前时间，自动切换到对应模型。

---

### 家庭成员

#### 建军 🐱
- **身份**: 家里的猫
- **品种**: 长毛曼基康金渐层
- **生日**: 2025年8月1日
- **性格**: 活泼
- **小红书账号**: 19101465631
- **素材目录**: `/Users/tongxiaotong/littleCat/`
- **专属 Agent**: `jianjun`（建军小助手）
  - 工作空间: `~/.openclaw/workspace/jianjun/`
  - 职责: 小红书运营、照片管理、内容创作

### 技术配置

#### GitHub
- **仓库**: https://github.com/NiklausTxt/openclaw-workspace
- **本地路径**: `~/.openclaw/workspace`
- **Git 用户**: NiklausTxt (tongxiaotong139@163.com)
- **认证**: GitHub CLI (gh) + 浏览器授权

#### Skills
- **GitHub 仓库管理**: `skills/github-repo/SKILL.md`
  - 使用 gh CLI 创建仓库、初始化 Git、配置认证、推送代码

### 自动化配置

#### Git 自动提交策略
1. **实时写入**: 重要操作时自动写入 memory/daily-notes/
2. **每小时同步**: 通过 hourly-sync cron 补漏
3. **每日摘要**: daily-summary cron 执行安全审计 + 提交推送
4. **大改动检测**: big-change-detector cron 自动提交重大变更

---

## 当前重要任务

### trading_simulation（A股模拟交易）
- **任务类型**: A股模拟交易
- **起始资金**: 100,000元
- **当前状态**: 空仓，现金100,000元
- **截止时间**: 2026-03-31
- **目标**: 风险可控前提下收益最大化
- **风险控制**: 单票≤30%，止损-5%

**🚨 下一步行动**: 2026-03-05 14:00 必须执行
- 观察市场（脑机接口、电力板块）
- 检查目标标的（麦澜德、翔宇医疗、世纪华通）
- 如满足条件，立即执行买入（仓位20-25%）
- 严格设置止损-5%，止盈+8%/+15%

**目标标的详情**:
1. 麦澜德（688883）: 当前42.27（+3.96%），目标≤42.00
2. 翔宇医疗（688610）: 当前64.03（+3.93%），目标≤63.50
3. 世纪华通（002602）: 当前17.98（+3.63%），目标≤17.50

**文档路径**: `~/.openclaw/workspace/trading_simulation/`
- REMINDER.md ⭐ 必须在14:00打开并执行
- execution_plan.md（下午执行计划）
- watchlist.md（观察名单）
- strategy.md（交易策略）

---

## 最近更新

**2026-03-04**
- 重构记忆文件系统，采用任务管理模式
- 创建飞书命令配置指南
- 实现任务切换、更新、关闭、查询机制

---

持续更新中。