# lark-cli base — Bitable Reference

## Common Flags

All base commands require `--base <base_token>` and usually `--table <table_id_or_name>`.

## Records

### +record-list
```bash
# Basic list
lark-cli base +record-list --base bascnXXX --table tblXXX --format table

# With filter
lark-cli base +record-list --base bascnXXX --table tblXXX \
  --filter '{"conjunction":"and","conditions":[{"field_name":"Status","operator":"is","value":["Done"]}]}' \
  --page-all

# With field selection and sort
lark-cli base +record-list --base bascnXXX --table tblXXX \
  --field-names "Name,Status,Due Date" \
  --sort '[{"field_name":"Due Date","desc":true}]'
```

### +record-get
```bash
lark-cli base +record-get --base bascnXXX --table tblXXX --record-id recXXX
```

### +record-upsert
```bash
# Create
lark-cli base +record-upsert --base bascnXXX --table tblXXX \
  --data '{"fields":{"Name":"New Item","Status":"Open"}}'

# Update (with record-id)
lark-cli base +record-upsert --base bascnXXX --table tblXXX --record-id recXXX \
  --data '{"fields":{"Status":"Closed"}}'
```

### +record-delete
```bash
lark-cli base +record-delete --base bascnXXX --table tblXXX --record-id recXXX
```

### +record-upload-attachment
```bash
lark-cli base +record-upload-attachment --base bascnXXX --table tblXXX \
  --record-id recXXX --field "Attachments" --file ./photo.jpg
```

## Data Query (Aggregation)

### +data-query
```bash
lark-cli base +data-query --base bascnXXX --table tblXXX \
  --data '{
    "filter":{"conjunction":"and","conditions":[{"field_name":"Status","operator":"is","value":["Done"]}]},
    "aggregate":{"field_name":"Amount","func":"SUM"},
    "group_by":[{"field_name":"Category"}]
  }'
```

## Tables

```bash
# List tables
lark-cli base +table-list --base bascnXXX --format table

# Create table
lark-cli base +table-create --base bascnXXX --name "Tasks" \
  --fields '[{"field_name":"Name","type":1},{"field_name":"Status","type":3}]'

# Delete table
lark-cli base +table-delete --base bascnXXX --table tblXXX
```

## Fields

```bash
# List fields
lark-cli base +field-list --base bascnXXX --table tblXXX --format table

# Create field
lark-cli base +field-create --base bascnXXX --table tblXXX \
  --data '{"field_name":"Priority","type":3,"property":{"options":[{"name":"P0"},{"name":"P1"},{"name":"P2"}]}}'

# Update field
lark-cli base +field-update --base bascnXXX --table tblXXX --field fldXXX \
  --data '{"field_name":"New Name"}'
```

### Field Types

| Type ID | Name | Notes |
|:--------|:-----|:------|
| 1 | Text | |
| 2 | Number | |
| 3 | SingleSelect | |
| 4 | MultiSelect | |
| 5 | DateTime | |
| 7 | Checkbox | |
| 11 | Person | |
| 13 | Phone | |
| 15 | URL | |
| 17 | Attachment | |
| 18 | SingleLink | |
| 20 | Formula | |
| 21 | DuplexLink | |
| 22 | Location | |
| 23 | GroupChat | |
| 1001 | CreatedTime | |
| 1002 | ModifiedTime | |
| 1003 | CreatedUser | |
| 1004 | ModifiedUser | |
| 1005 | AutoNumber | |

## Views

```bash
lark-cli base +view-list --base bascnXXX --table tblXXX --format table
lark-cli base +view-create --base bascnXXX --table tblXXX --name "My View" --type grid
lark-cli base +view-get-filter --base bascnXXX --table tblXXX --view vewXXX
lark-cli base +view-set-filter --base bascnXXX --table tblXXX --view vewXXX \
  --data '{"conjunction":"and","conditions":[{"field_name":"Status","operator":"is","value":["Open"]}]}'
```

## Dashboards

```bash
lark-cli base +dashboard-list --base bascnXXX --format table
lark-cli base +dashboard-create --base bascnXXX --name "Overview"
```

## Workflows

```bash
lark-cli base +workflow-list --base bascnXXX
lark-cli base +workflow-get --base bascnXXX --workflow-id <id>
lark-cli base +workflow-enable --base bascnXXX --workflow-id <id>
lark-cli base +workflow-disable --base bascnXXX --workflow-id <id>
```

## Filter Syntax

```json
{
  "conjunction": "and",
  "conditions": [
    {
      "field_name": "Status",
      "operator": "is",
      "value": ["Open"]
    },
    {
      "field_name": "Priority",
      "operator": "is",
      "value": ["P0", "P1"]
    }
  ]
}
```

**Operators:** `is`, `isNot`, `contains`, `doesNotContain`, `isEmpty`, `isNotEmpty`, `isGreater`, `isLess`, `isGreaterEqual`, `isLessEqual`
