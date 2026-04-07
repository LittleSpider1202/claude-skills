# lark-cli sheets — Spreadsheet Reference

## Smart Commands

### +info
```bash
# Get spreadsheet info (sheets list, properties)
lark-cli sheets +info --spreadsheet <token>
```

### +read
```bash
# Read a range
lark-cli sheets +read --spreadsheet <token> --range "Sheet1!A1:D10"

# Read entire sheet
lark-cli sheets +read --spreadsheet <token> --range "Sheet1"

# Output as table
lark-cli sheets +read --spreadsheet <token> --range "Sheet1!A1:D10" --format table

# Output as CSV
lark-cli sheets +read --spreadsheet <token> --range "Sheet1" --format csv
```

### +write
```bash
# Write values (overwrite mode)
lark-cli sheets +write --spreadsheet <token> --range "Sheet1!A1:B2" \
  --data '{"values":[["Name","Score"],["Alice",95]]}'
```

### +append
```bash
# Append rows
lark-cli sheets +append --spreadsheet <token> --range "Sheet1!A:D" \
  --data '{"values":[["Bob",88,"Engineering","2024-01-15"],["Carol",92,"Design","2024-01-16"]]}'
```

### +find
```bash
# Find cells matching a value
lark-cli sheets +find --spreadsheet <token> --sheet "Sheet1" --find "keyword"
```

### +create
```bash
# Create a new spreadsheet
lark-cli sheets +create --title "Q1 Report" --folder <folder_token>

# Create with header row
lark-cli sheets +create --title "Data" --folder <folder_token> \
  --headers '["Name","Email","Role","Start Date"]'

# Create with initial data
lark-cli sheets +create --title "Data" --folder <folder_token> \
  --headers '["Name","Score"]' \
  --data '[["Alice",95],["Bob",88]]'
```

### +export
```bash
# Export as xlsx
lark-cli sheets +export --spreadsheet <token> --type xlsx -o ./report.xlsx

# Export as csv
lark-cli sheets +export --spreadsheet <token> --type csv -o ./data.csv
```

## Raw API Examples

```bash
# Add a new sheet
lark-cli api POST /open-apis/sheets/v3/spreadsheets/<token>/sheets \
  --data '{"sheet":{"title":"New Sheet"}}'

# Delete a sheet
lark-cli api DELETE /open-apis/sheets/v3/spreadsheets/<token>/sheets/<sheet_id>

# Set cell style
lark-cli api PUT /open-apis/sheets/v2/spreadsheets/<token>/style \
  --data '{"appendStyle":{"range":"Sheet1!A1:D1","style":{"bold":true,"backColor":"#F0F0F0"}}}'

# Set filter
lark-cli api POST /open-apis/sheets/v3/spreadsheets/<token>/sheets/<sheet_id>/filter \
  --data '{"range":"Sheet1!A1:D100","col":"A","condition":{"filter_type":"text","compare_type":"contains","expected":["error"]}}'
```

## Notes

- Range format: `SheetName!A1:D10` or `SheetName` (entire sheet) or `SheetName!A:D` (full columns)
- Sheet name with spaces must be quoted in range: `'My Sheet'!A1:D10`
- Values are 2D arrays: `[[row1col1, row1col2], [row2col1, row2col2]]`
