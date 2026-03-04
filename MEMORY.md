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

### 家庭成员

#### 建军 🐱
- **身份**: 家里的猫
- **品种**: 长毛曼基康金渐层
- **生日**: 2025年8月1日
- **性格**: 活泼
- **小红书账号**: 19101465631
- **素材目录**: `/Users/tongxiaotong/littleCat/`

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

## 最近更新

**2026-03-04**
- 重构记忆文件系统，采用任务管理模式
- 创建飞书命令配置指南
- 实现任务切换、更新、关闭、查询机制

---

持续更新中。