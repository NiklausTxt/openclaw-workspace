# Memory 目录结构

## 📁 目录组织

```
memory/
├── README.md                  # 本文件
├── MEMORY.md                  # 长期记忆（精炼的知识、决策、配置）
├── daily-notes/               # 按日期组织的日常记录
│   ├── 2026-03-02.md         # 2026-03-02的原始日志
│   ├── 2026-03-03.md         # 2026-03-03的原始日志
│   ├── 2026-03-04.md         # 2026-03-04的原始日志
│   └── ...
├── projects/                  # 项目相关的记录
│   ├── jianjun-xiaohongshu/   # 建军小红书运营项目
│   │   ├── 2026-03-02-xiaohongshu-note-upload.md
│   │   └── ...
│   └── daily-life/            # 日常闲聊和其他内容（默认项目）
│       ├── 2026-03-04-stock-automation.md
│       └── ...
└── archive/                   # 归档的旧记录（超过30天）
    └── ...
```

## 📝 文件说明

### daily-notes/
按日期组织的原始日志，记录每天的所有事件和操作：

- **事件** - 按时间线记录的对话和操作
- **操作记录** - 表格形式记录exec命令
- **⚠️ 敏感信息访问** - 敏感操作追踪
- **备注** - 其他补充

**命名规则**: `YYYY-MM-DD.md`

### projects/
项目相关的详细记录：

- **jianjun-xiaohongshu/** - 建军小红书运营项目的所有记录
  - 笔记上传
  - 直播调研
  - 内容策略
  - 数据分析
- **daily-life/** - 日常闲聊和其他内容（默认项目）
  - 股票交易
  - 技术设置
  - 其他临时项目

### MEMORY.md
从daily notes和projects中提炼出的长期记忆：

- 家庭成员信息
- GitHub配置
- 自动化配置
- 重要决策和经验

### archive/
超过30天的daily notes移到这里，保持memory目录整洁。

## 🔍 使用指南

### 新记录的创建

1. **daily-notes** - 每天的自动同步会创建/更新 `YYYY-MM-DD.md`
2. **projects** - 重要项目内容会在对应项目目录创建独立文件

### 查找历史记录

1. **按日期查找** - 查看 `daily-notes/YYYY-MM-DD.md`
2. **按项目查找** - 查看 `projects/[项目名]/`
3. **长期记忆** - 查看 `MEMORY.md`

### 归档规则

- daily-notes超过30天的文件移到 `archive/`
- archive按年份子目录组织：`archive/2026/`、`archive/2027/` 等

## 🔄 维护建议

- **每日** - hourly-sync cron 自动更新 daily-notes
- **每周** - 检查projects分类是否准确
- **每月** - 归档旧的daily notes到archive
- **每季度** - 更新MEMORY.md，提炼长期记忆
