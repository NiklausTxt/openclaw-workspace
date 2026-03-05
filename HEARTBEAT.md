# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

## 下午交易任务（trading_simulation）

### 2026-03-05 14:00 必须执行

**优先级**: 最高 ⭐⭐⭐

#### 14:00-14:30: 观察市场
- [ ] 打开 `~/.openclaw/workspace/trading_simulation/REMINDER.md` ⭐ 必须执行
- [ ] 打开 `~/.openclaw/workspace/trading_simulation/watchlist.md`
- [ ] 使用browser访问同花顺获取实时行情
- [ ] 观察脑机接口板块涨幅（目标：回落至3%以下）
- [ ] 观察目标标的：
  - 麦澜德（688883）: 当前42.27，目标≤42.00
  - 翔宇医疗（688610）: 当前64.03，目标≤63.50
  - 世纪华通（002602）: 当前17.98，目标≤17.50
- [ ] 观察电力板块涨幅
- [ ] 判断是否满足买入条件（方案A/B/C）

#### 14:30-15:00: 执行交易
- [ ] 如满足方案A（脑机接口），立即执行买入
- [ ] 如满足方案B（电力），立即执行买入
- [ ] 记录买入信息
- [ ] 设置止损-5%，止盈+8%（减仓50%）、+15%（全部）
- [ ] 更新相关文档

#### 15:00-15:30: 检查与复盘
- [ ] 检查成交情况
- [ ] 更新capital_status.md
- [ ] 更新daily_log.md
- [ ] 复盘交易
- [ ] 总结经验

---

**⚠️ 重要**: 下午14:00必须打开REMINDER.md并执行！
