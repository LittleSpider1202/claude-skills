# lark-cli im — Messaging Reference

## Smart Commands (+)

### +messages-send
Send a message (bot identity).

```bash
# Text to chat
lark-cli im +messages-send --chat-id oc_xxx --text "Hello"

# Markdown to user
lark-cli im +messages-send --user-id ou_xxx --markdown "**Bold** message"

# Rich post (title + content blocks)
lark-cli im +messages-send --chat-id oc_xxx --post-title "Alert" --post-content '[["text","Server is down"],["a","Dashboard","https://example.com"]]'

# Image
lark-cli im +messages-send --chat-id oc_xxx --image ./screenshot.png

# File
lark-cli im +messages-send --chat-id oc_xxx --file ./report.pdf

# With idempotency key (prevents duplicates)
lark-cli im +messages-send --chat-id oc_xxx --text "Hello" --uuid "unique-key-123"
```

**Flags:** `--chat-id`, `--user-id` (pick one), `--text`, `--markdown`, `--post-title`, `--post-content`, `--image`, `--file`, `--uuid`

### +messages-reply
Reply to a message (supports thread replies).

```bash
lark-cli im +messages-reply --message-id om_xxx --text "Got it"
lark-cli im +messages-reply --message-id om_xxx --text "Thread reply" --in-thread
```

**Flags:** `--message-id`, `--text`, `--markdown`, `--in-thread`, `--uuid`

### +messages-search
Search messages (user identity).

```bash
lark-cli im +messages-search --query "project update" --format table
lark-cli im +messages-search --query "bug" --chat-id oc_xxx --from ou_xxx --start "2024-01-01" --end "2024-12-31"
```

**Flags:** `--query`, `--chat-id`, `--from`, `--start`, `--end`, `--type` (message type filter)

### +messages-mget
Batch get messages by IDs.

```bash
lark-cli im +messages-mget --message-ids "om_xxx,om_yyy,om_zzz"
```

### +messages-resources-download
Download images/files from a message.

```bash
lark-cli im +messages-resources-download --message-id om_xxx --file-key <key> -o ./downloaded.png
```

### +chat-search
Search group chats by keyword.

```bash
lark-cli im +chat-search --query "engineering" --format table
```

### +chat-create
Create a group chat (bot identity).

```bash
lark-cli im +chat-create --name "Project Chat" --user-ids "ou_xxx,ou_yyy"
```

### +chat-update
Update group chat name/description.

```bash
lark-cli im +chat-update --chat-id oc_xxx --name "New Name" --description "Updated desc"
```

### +chat-messages-list
List messages in a chat.

```bash
lark-cli im +chat-messages-list --chat-id oc_xxx --page-all --format table
lark-cli im +chat-messages-list --user-id ou_xxx  # P2P conversation
```

### +threads-messages-list
List messages in a thread.

```bash
lark-cli im +threads-messages-list --message-id om_xxx
```

## Raw Resource Commands

For operations not covered by smart commands:

```bash
# List chat members
lark-cli im chat.members list --params '{"chat_id":"oc_xxx"}' --page-all

# Pin a message
lark-cli im pins create --data '{"chat_id":"oc_xxx","message_id":"om_xxx"}'

# Add reaction
lark-cli im reactions create --params '{"message_id":"om_xxx"}' --data '{"reaction_type":{"emoji_type":"THUMBSUP"}}'
```
