# MEMORY.md - 长期记忆

## Memory 目录结构

从2026-03-04开始，memory目录重新组织为：

```
memory/
├── README.md                  # 本目录使用说明
├── MEMORY.md                  # 本文件 - 长期记忆
├── daily-notes/               # 按日期组织的日常记录（自动同步）
│   ├── 2026-03-02.md
│   └── ...
├── projects/                  # 项目相关记录
│   ├── INDEX.md              # 项目索引
│   ├── jianjun-xiaohongshu/  # 建军小红书运营项目
│   └── daily-life/           # 日常闲聊和其他内容（默认项目）
└── archive/                   # 归档的旧记录（超过30天）
```

### 详细说明
- **daily-notes/** - 每天的原始日志，包括事件、操作记录、敏感信息访问
- **projects/jianjun-xiaohongshu/** - 建军小红书运营专项
- **projects/daily-life/** - 股票交易、技术设置、其他内容
- **MEMORY.md** - 从daily notes和projects提炼的长期记忆（本文件）

详见 `memory/README.md`

---

## 家庭成员

### 建军 🐱
- **身份**: 家里的猫
- **品种**: 长毛曼基康金渐层
- **生日**: 2025年8月1日
- **性格**: 活泼
- **小红书账号**: 19101465631
- **素材目录**: `/Users/tongxiaotong/littleCat/`

## GitHub 配置

- **仓库**: https://github.com/NiklausTxt/openclaw-workspace
- **本地路径**: `~/.openclaw/workspace`
- **Git 用户**: NiklausTxt (tongxiaotong139@163.com)
- **认证**: GitHub CLI (gh) + 浏览器授权

## Skills 目录

- **GitHub 仓库管理**：`skills/github-repo/SKILL.md`
  - 使用 gh CLI 创建仓库、初始化 Git、配置认证、推送代码
  - 包含常见问题解决（SSH/HTTPS 认证、超时等）
  - 以后需要 Git/GitHub 操作时自动读取此 skill

## 自动化配置

### Git 自动提交策略（两者结合）

1. **实时写入**：重要操作时自动写入 memory/YYYY-MM-DD.md
   - 执行 exec 命令
   - 访问敏感文件（密码、token、账号）
   - 修改配置文件
   - 记录重要决策

2. **每小时同步**：通过 hourly-sync cron 补漏
   - 时间：每小时 00 分
   - 任务：读取 sessions history，提取重要事件
   - 标注：【自动同步】

3. **每日摘要 + 提交**：daily-summary cron
   - 时间：每天 00:05
   - 任务：安全审计摘要 + git 提交推送

4. **大改动检测**：big-change-detector cron
   - 时间：每 2 小时
   - 条件：重要文件变更或 >5 个新文件
   - 动作：自动提交推送 + 通知

---

持续更新中。
