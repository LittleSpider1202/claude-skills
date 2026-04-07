# feishu-hook-notify — Claude Code Event to Feishu

Global hook skill: sends Feishu notification when Claude Code stops (task complete / permission needed).

## Setup

1. Set env vars (optional, has built-in defaults):
   - `FEISHU_WEBHOOK_URL` — Feishu bot webhook URL
   - `FEISHU_SIGN_SECRET` — Webhook signing secret

2. Hook is registered in `~/.claude/settings.json` under `hooks.Stop`.

## Usage

```bash
# Manual test
python3 ~/.claude/skills/feishu-hook-notify/scripts/hook_notify.py stop
python3 ~/.claude/skills/feishu-hook-notify/scripts/hook_notify.py permission
python3 ~/.claude/skills/feishu-hook-notify/scripts/hook_notify.py "Custom message here"
```

## Hook Events

| Event | Trigger | Feishu Message |
|-------|---------|----------------|
| `stop` | Claude Code Stop hook | "Claude Code Stopped — check terminal" |
| `permission` | (future) permission hook | "Permission Required" |
| custom | Manual invocation | Custom text |
