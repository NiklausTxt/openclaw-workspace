# MEMORY.md - 长期记忆

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
