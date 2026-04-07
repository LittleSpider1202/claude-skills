# lark-cli calendar & task — Reference

## Calendar

### +agenda
```bash
# Today's agenda
lark-cli calendar +agenda

# Specific date range
lark-cli calendar +agenda --start "2024-03-01" --end "2024-03-07"

# Table format
lark-cli calendar +agenda --format table
```

### +create
```bash
# Create event
lark-cli calendar +create --summary "Team Standup" \
  --start "2024-03-15 09:00" --end "2024-03-15 09:30"

# With attendees
lark-cli calendar +create --summary "Review Meeting" \
  --start "2024-03-15 14:00" --end "2024-03-15 15:00" \
  --attendees "ou_xxx,ou_yyy"

# All-day event
lark-cli calendar +create --summary "Team Offsite" \
  --start "2024-03-20" --end "2024-03-21" --all-day

# With location and description
lark-cli calendar +create --summary "Workshop" \
  --start "2024-03-15 10:00" --end "2024-03-15 12:00" \
  --location "Room 301" --description "Bring your laptop"
```

### +freebusy
```bash
# Check if users are free
lark-cli calendar +freebusy --user-ids "ou_xxx,ou_yyy" \
  --start "2024-03-15 09:00" --end "2024-03-15 18:00"
```

### +suggestion
```bash
# Suggest meeting times
lark-cli calendar +suggestion --user-ids "ou_xxx,ou_yyy" \
  --start "2024-03-15" --end "2024-03-16" --duration 60
```

## Task

### +create
```bash
# Simple task
lark-cli task +create --summary "Review PR #42"

# With due date and assignee
lark-cli task +create --summary "Deploy v2.0" \
  --due "2024-03-20 17:00" --members "ou_xxx"

# With description
lark-cli task +create --summary "Write docs" \
  --description "Cover API endpoints and auth flow"
```

### +get-my-tasks
```bash
lark-cli task +get-my-tasks --format table
lark-cli task +get-my-tasks --completed false --format table
```

### +update
```bash
lark-cli task +update --task-id <task_id> --summary "Updated title"
lark-cli task +update --task-id <task_id> --due "2024-03-25 12:00"
```

### +complete / +reopen
```bash
lark-cli task +complete --task-id <task_id>
lark-cli task +reopen --task-id <task_id>
```

### +assign
```bash
# Add assignee
lark-cli task +assign --task-id <task_id> --add "ou_xxx"

# Remove assignee
lark-cli task +assign --task-id <task_id> --remove "ou_xxx"
```

### +comment
```bash
lark-cli task +comment --task-id <task_id> --content "Blocked by infra issue"
```

### +reminder
```bash
lark-cli task +reminder --task-id <task_id> --relative-fire-minute 30
```

### +followers
```bash
lark-cli task +followers --task-id <task_id> --add "ou_xxx,ou_yyy"
```

## Task Lists

```bash
# Create task list
lark-cli task +tasklist-create --name "Sprint 23"

# Add tasks to list
lark-cli task +tasklist-task-add --tasklist-id <id> --task-ids "<task1>,<task2>"

# Manage members
lark-cli task +tasklist-members --tasklist-id <id> --add "ou_xxx" --role editor
```
