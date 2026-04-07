# lark-cli api, auth & contact — Reference

## auth: Authentication

```bash
# Check current status
lark-cli auth status

# Login (device flow)
lark-cli auth login

# List logged-in users
lark-cli auth list

# Check if token has specific scopes
lark-cli auth check --scopes "im:message,calendar:calendar"

# Query all enabled scopes
lark-cli auth scopes

# Logout
lark-cli auth logout
```

## contact: User Operations

### +search-user
```bash
# Search by name or email
lark-cli contact +search-user --query "John" --format table
lark-cli contact +search-user --query "john@example.com"
```

### +get-user
```bash
# Get current user info
lark-cli contact +get-user

# Get specific user
lark-cli contact +get-user --user-id ou_xxx
```

## api: Generic API Calls

For any Lark Open API not covered by smart commands.

```bash
lark-cli api <METHOD> <path> [flags]
```

### Flags
- `--params <json>` — query parameters
- `--data <json>` — request body (POST/PATCH/PUT/DELETE)
- `--as user|bot|auto` — identity type
- `--format json|table|csv|ndjson|pretty` — output format
- `--page-all` — auto-paginate
- `--page-size <N>` — items per page
- `--page-limit <N>` — max pages (default 10, 0=unlimited)
- `--page-delay <MS>` — delay between pages (default 200)
- `-o, --output <path>` — output file for binary responses
- `--dry-run` — print request without executing

### Examples

```bash
# List calendars
lark-cli api GET /open-apis/calendar/v4/calendars

# Get user info
lark-cli api GET /open-apis/contact/v3/users/ou_xxx

# Create a wiki node
lark-cli api POST /open-apis/wiki/v2/spaces/<space_id>/nodes \
  --data '{"obj_type":"docx","parent_node_token":"<parent>"}'

# List wiki spaces
lark-cli api GET /open-apis/wiki/v2/spaces --page-all --format table

# Get event subscriptions
lark-cli api GET /open-apis/event/v1/subscriptions --as bot

# Batch operation
lark-cli api POST /open-apis/bitable/v1/apps/<base>/tables/<table>/records/batch_create \
  --data '{"records":[{"fields":{"Name":"A"}},{"fields":{"Name":"B"}}]}'
```

## schema: API Schema Lookup

```bash
# Look up method parameters
lark-cli schema calendar.events.list --format pretty
lark-cli schema im.messages.create --format pretty
lark-cli schema bitable.records.search --format pretty
```

Use schema to discover exact parameter names and required scopes before making API calls.

## config: CLI Configuration

```bash
# Show current config
lark-cli config list

# Set a config value
lark-cli config set <key> <value>
```
