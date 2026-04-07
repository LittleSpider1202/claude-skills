"""Claude Code Hook -> Feishu notification with delayed queue.

When a hook fires, instead of sending immediately:
1. Write a pending file with timestamp + message data
2. Spawn a background process that sleeps DELAY seconds
3. After DELAY, check if the pending file's timestamp still matches
   - Match → user didn't respond → send notification
   - Mismatch → user responded (new hook overwrote) → exit silently

This avoids noisy notifications when the user is actively working.

Usage:
    hook_notify.py stop             # Called by Stop hook
    hook_notify.py permission       # Called by PreToolUse hook
    hook_notify.py --deferred KEY   # Internal: background deferred sender

Env vars:
    FEISHU_WEBHOOK_URL   - Webhook URL
    FEISHU_SIGN_SECRET   - Signing secret
    FEISHU_DELAY_SECONDS - Delay before sending (default: 60)
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

# ---------- config ----------

WEBHOOK_URL = os.environ.get(
    "FEISHU_WEBHOOK_URL",
    "https://open.feishu.cn/open-apis/bot/v2/hook/c885322f-7509-4fae-9e4f-d3fe98e27796",
)
SIGN_SECRET = os.environ.get("FEISHU_SIGN_SECRET", "UaYOuESOH4liSBC91FUfGb")
DELAY_SECONDS = int(os.environ.get("FEISHU_DELAY_SECONDS", "60"))

PENDING_DIR = Path.home() / ".claude" / "feishu-notify-pending"
PYTHON_EXE = sys.executable
SCRIPT_PATH = str(Path(__file__).resolve())

_SAFE_CMD_PREFIXES = (
    "ls ", "cat ", "head ", "tail ", "echo ", "pwd", "which ",
    "find ", "wc ", "sort ", "uniq ", "diff ", "file ",
    "git status", "git log", "git diff", "git branch",
    "git show", "git stash list",
    "pytest", "python",
)

# ---------- signing ----------

def _gen_sign(timestamp: int, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(hmac_code).decode("utf-8")

# ---------- send ----------

def send(title: str, content: str, color: str = "orange") -> dict:
    timestamp = int(time.time())
    sign = _gen_sign(timestamp, SIGN_SECRET)

    payload = {
        "timestamp": str(timestamp),
        "sign": sign,
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": color,
            },
            "elements": [
                {"tag": "markdown", "content": content},
            ],
        },
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(
        WEBHOOK_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

# ---------- pending file management ----------

def _pending_path(key: str) -> Path:
    return PENDING_DIR / f"{key}.json"


def _write_pending(key: str, data: dict) -> str:
    """Write pending notification. Returns the unique timestamp key."""
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    ts = str(time.time())
    data["_ts"] = ts
    _pending_path(key).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return ts


def _read_pending(key: str) -> dict | None:
    p = _pending_path(key)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def _clear_pending(key: str) -> None:
    p = _pending_path(key)
    if p.exists():
        p.unlink(missing_ok=True)

# ---------- deferred sender (background process) ----------

def _run_deferred(key: str, expected_ts: str) -> None:
    """Sleep, then check if pending file still matches. If so, send."""
    time.sleep(DELAY_SECONDS)

    pending = _read_pending(key)
    if pending is None:
        return  # cancelled
    if pending.get("_ts") != expected_ts:
        return  # overwritten by newer event, skip

    title = pending.get("title", "Claude Code 通知")
    content = pending.get("content", "请检查终端。")
    color = pending.get("color", "orange")

    try:
        result = send(title, content, color)
        if result.get("code", -1) == 0:
            _clear_pending(key)
    except Exception:
        pass


def _spawn_deferred(key: str, expected_ts: str) -> None:
    """Spawn a detached background process to send after delay."""
    cmd = [PYTHON_EXE, SCRIPT_PATH, "--deferred", key, expected_ts]
    # CREATE_NEW_PROCESS_GROUP on Windows, start_new_session on Unix
    kwargs = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    else:
        kwargs["start_new_session"] = True

    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        **kwargs,
    )

# ---------- context extraction ----------

def _read_stdin() -> dict:
    try:
        raw = sys.stdin.read()
        if raw.strip():
            return json.loads(raw)
    except Exception:
        pass
    return {}


def _is_safe_command(cmd: str) -> bool:
    cmd_stripped = cmd.strip()
    for prefix in _SAFE_CMD_PREFIXES:
        if cmd_stripped.startswith(prefix):
            return True
    return False


def _extract_last_text(ctx: dict) -> str:
    for key in ("message", "response", "content", "output"):
        val = ctx.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
        if isinstance(val, dict):
            for sub in ("content", "text", "output"):
                s = val.get(sub)
                if isinstance(s, str) and s.strip():
                    return s.strip()
            c = val.get("content")
            if isinstance(c, list):
                texts = []
                for block in c:
                    if isinstance(block, str):
                        texts.append(block)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        texts.append(block.get("text", ""))
                if texts:
                    return "\n".join(texts).strip()

    tool_input = ctx.get("tool_input", {})
    if isinstance(tool_input, dict):
        cmd = tool_input.get("command", "")
        fp = tool_input.get("file_path", "")
        if cmd:
            return f"执行命令: {cmd}"
        if fp:
            return f"操作文件: {fp}"
    return ""


def _truncate(text: str, max_len: int = 200) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def _detect_event_type(ctx: dict, text: str) -> str:
    tool = ctx.get("tool", "")
    if tool:
        return "permission"

    lower = text.lower()
    permission_signals = ["确认", "approve", "deny", "permission", "允许", "是否继续", "请确认", "y/n"]
    question_signals = ["？", "?", "请问", "需要你", "你想", "要不要", "选择哪"]
    done_signals = ["完成", "done", "finished", "已完成", "搞定", "已 commit", "已提交"]

    if any(s in lower for s in permission_signals):
        return "permission"
    if any(s in lower for s in done_signals):
        return "done"
    if any(s in lower for s in question_signals):
        return "question"
    return "done"

# ---------- message formatting ----------

def _build_message(event: str, ctx: dict, project: str) -> tuple[str, str, str]:
    """Returns (title, content, color)."""
    text = _extract_last_text(ctx)
    summary = _truncate(text) if text else ""
    tool = ctx.get("tool", "")

    if event == "permission":
        title = "🔐 需要授权"
        tool_desc = f"**{tool}**" if tool else "某项操作"
        body = f"执行 {tool_desc} 时需要您的授权，请回到终端处理。"
        if summary:
            body += f"\n\n**上下文**：{summary}"
        return title, body + f"\n\n📁 项目：`{project}`", "orange"

    detected = _detect_event_type(ctx, text)

    if detected == "permission":
        title = "🔐 需要授权"
        body = "Claude 等待您的授权，请回到终端处理。"
        if summary:
            body += f"\n\n**上下文**：{summary}"
        return title, body + f"\n\n📁 项目：`{project}`", "orange"

    if detected == "question":
        title = "💬 等待您的回复"
        body = "Claude 有问题需要您确认。"
        if summary:
            body += f"\n\n**问题**：{summary}"
        return title, body + f"\n\n📁 项目：`{project}`", "blue"

    title = "✅ 任务已完成"
    body = "Claude 已完成当前任务。"
    if summary:
        body += f"\n\n**摘要**：{summary}"
    return title, body + f"\n\n📁 项目：`{project}`", "green"

# ---------- main ----------

def main() -> None:
    args = sys.argv[1:]

    # Internal deferred mode: hook_notify.py --deferred <key> <ts>
    if len(args) >= 3 and args[0] == "--deferred":
        _run_deferred(args[1], args[2])
        return

    event = args[0] if args else "stop"
    cwd = os.environ.get("PWD", os.getcwd())
    project = os.path.basename(cwd)
    ctx = _read_stdin()

    # For PreToolUse: skip safe commands, pass through stdin
    if event == "permission":
        tool_input = ctx.get("tool_input", {})
        cmd = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
        if _is_safe_command(cmd):
            print(json.dumps(ctx))
            return
        print(json.dumps(ctx))

    title, content, color = _build_message(event, ctx, project)

    # Write pending + spawn deferred sender (delayed queue)
    pending_key = event  # "stop" or "permission" — one slot per event type
    ts = _write_pending(pending_key, {
        "title": title,
        "content": content,
        "color": color,
    })
    _spawn_deferred(pending_key, ts)
    print(f"[feishu-hook] Queued ({DELAY_SECONDS}s delay): {title}", file=sys.stderr)


if __name__ == "__main__":
    main()
