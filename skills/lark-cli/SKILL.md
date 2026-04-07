---
name: lark-cli
description: Lark/Feishu CLI tool for messaging, documents, spreadsheets, bitable, calendar, tasks, and generic API calls. Use when the user wants to interact with Lark/Feishu — send messages, read docs, query bitable records, manage calendar events, upload files, or call any Lark Open API.
allowed-tools: Bash
---

# lark-cli — Lark/Feishu CLI

`lark-cli` is a CLI tool for interacting with the Lark (Feishu) Open Platform. It wraps the Lark Open API into ergonomic subcommands.

## Quick Start

```bash
# Check auth status
lark-cli auth status

# Send a message
lark-cli im +messages-send --chat-id <chat_id> --text "Hello"

# Read a spreadsheet
lark-cli sheets +read --spreadsheet <token> --range "Sheet1!A1:D10"

# Query bitable records
lark-cli base +record-list --base <base_token> --table <table_id>

# Generic API call
lark-cli api GET /open-apis/calendar/v4/calendars
```

## Core Concepts

### Identity: `--as user | bot | auto`

Most commands default to `--as auto`. Use `--as user` for user-scoped ops (search, calendar agenda) and `--as bot` for bot-scoped ops (send messages).

### Output: `--format json | table | csv | ndjson | pretty`

Default is `json`. Use `--format table` for human-readable output, `--format csv` for piping.

### Pagination: `--page-all --page-size N --page-limit N`

Add `--page-all` to automatically fetch all pages. `--page-limit` caps the number of pages (default 10).

### Token Types

| Token prefix | Resource |
|:------------|:---------|
| `oc_` | Chat ID |
| `ou_` | Open User ID |
| `om_` | Message ID |
| `omt_` | Thread ID |
| `bascn...` | Base (Bitable) token |
| `tbl...` | Table ID |
| `fld...` | Field ID |
| `rec...` | Record ID |
| `vew...` | View ID |

### Schema Lookup

Use `lark-cli schema <service.resource.method> --format pretty` to inspect any API method's parameters, types, and required scopes before calling it.

## Command Modules

| Module | Description | Reference |
|:-------|:-----------|:----------|
| `im` | Messages, chats, threads, reactions, pins | [references/im.md](references/im.md) |
| `base` | Bitable: tables, fields, records, views, dashboards, workflows | [references/base.md](references/base.md) |
| `docs` | Documents: create, fetch, update, search | [references/docs-drive.md](references/docs-drive.md) |
| `drive` | Files: upload, download, comments, permissions | [references/docs-drive.md](references/docs-drive.md) |
| `sheets` | Spreadsheets: read, write, append, find, export | [references/sheets.md](references/sheets.md) |
| `calendar` | Events, agenda, free/busy, scheduling | [references/calendar-task.md](references/calendar-task.md) |
| `task` | Tasks, task lists, subtasks, assignments | [references/calendar-task.md](references/calendar-task.md) |
| `contact` | User search, user info | [references/api-auth.md](references/api-auth.md) |
| `api` | Generic REST API calls | [references/api-auth.md](references/api-auth.md) |
| `auth` | Login, logout, scopes, status | [references/api-auth.md](references/api-auth.md) |

## Workflow Patterns

### Send a message to a user by email

```bash
# 1. Find the user's open_id
lark-cli contact +search-user --query "someone@example.com" --format table

# 2. Send direct message (bot identity)
lark-cli im +messages-send --user-id <ou_xxx> --text "Hello from bot"
```

### Read bitable records with filter

```bash
lark-cli base +record-list --base <token> --table <table_id> \
  --filter '{"conjunction":"and","conditions":[{"field_name":"Status","operator":"is","value":["Done"]}]}' \
  --page-all --format table
```

### Upload file then share link

```bash
# Upload
lark-cli drive +upload --file ./report.pdf --parent <folder_token>

# Add permission
lark-cli api POST /open-apis/drive/v1/permissions/<file_token>/members \
  --data '{"member_type":"openchat","member_id":"oc_xxx","perm":"view"}'
```

## Tips

- Run `lark-cli <module> <command> --help` for full flag documentation of any command.
- Use `--dry-run` to preview the API request without executing.
- For commands not covered by built-in shortcuts, use `lark-cli api <METHOD> <path>`.
- Prefer `+` prefixed commands (smart shortcuts) over raw resource commands when available.
