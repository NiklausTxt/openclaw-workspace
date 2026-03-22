# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 建军相关

- **专属 Agent**: `jianjun` — 建军小助手（小红书运营、照片管理）
- **Agent 工作空间**: `~/.openclaw/workspace/jianjun/`
- **档案**: `jianjun/MEMORY.md` — 建军档案 + 运营记录
- **照片工作副本**: `jianjun/jianjun_photos/` — 建军照片
- **原始素材**: `/Users/tongxiaotong/littleCat/` — 照片、视频等原始素材

**使用方式**: 
- 在聊天中提到"建军"相关事项时，我会调用 jianjun agent
- 或直接说"让建军小助手处理"

## ACP Harness 配置

- **默认工作目录**: `/Users/tongxiaotong/solo` — Claude Code / Codex 代码任务默认项目地址
- **可用 Agent**: `claude`, `codex`
- **启动方式**: ACP Runtime（`sessions_spawn` + `runtime: "acp"`）

**使用规则**:
- 所有代码任务（Claude Code / Codex）默认使用 `/Users/tongxiaotong/solo` 作为工作目录
- 除非用户明确指定其他路径
- 自动传入 `cwd: "/Users/tongxiaotong/solo"` 参数
