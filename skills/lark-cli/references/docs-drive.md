# lark-cli docs & drive — Documents & Files Reference

## docs: Document Operations

### +create
```bash
# Create empty doc
lark-cli docs +create --title "Meeting Notes" --folder <folder_token>

# Create with initial content (markdown-like)
lark-cli docs +create --title "Report" --folder <folder_token> \
  --body "# Section 1\nContent here"
```

### +fetch
```bash
# Fetch by document token
lark-cli docs +fetch --document <doc_token>

# Fetch by URL (auto-extracts token)
lark-cli docs +fetch --url "https://xxx.feishu.cn/docx/xxxxxx"

# Output as plain text
lark-cli docs +fetch --document <doc_token> --format pretty
```

### +update
```bash
lark-cli docs +update --document <doc_token> \
  --data '{"requests":[{"insert_text":{"text":"Hello","location":{"zone_id":"0","index":0}}}]}'
```

### +search
```bash
# Search docs by keyword
lark-cli docs +search --query "quarterly report" --format table

# Filter by type
lark-cli docs +search --query "design" --type docx
```

**Types:** `doc`, `docx`, `sheet`, `bitable`, `wiki`, `slide`, `mindnote`

### +media-download
```bash
lark-cli docs +media-download --document <doc_token> --block-id <block_id> -o ./image.png
```

### +media-insert
```bash
lark-cli docs +media-insert --document <doc_token> --file ./diagram.png
```

## drive: File Operations

### +upload
```bash
lark-cli drive +upload --file ./presentation.pptx --parent <folder_token>
```

### +download
```bash
lark-cli drive +download --file <file_token> -o ./downloaded.pdf
```

### +add-comment
```bash
# Full-document comment
lark-cli drive +add-comment --file <token> --content "Please review this section"

# Comment on specific text in a docx
lark-cli drive +add-comment --file <token> --quote "specific text" --content "Needs revision"
```

## Raw API Examples

```bash
# List files in a folder
lark-cli api GET /open-apis/drive/v1/files \
  --params '{"folder_token":"<folder>"}' --page-all

# Get file metadata
lark-cli api POST /open-apis/drive/v1/metas/batch_query \
  --data '{"request_docs":[{"doc_token":"<token>","doc_type":"docx"}]}'

# Create folder
lark-cli api POST /open-apis/drive/v1/files/create_folder \
  --data '{"name":"New Folder","folder_token":"<parent>"}'

# Share file
lark-cli api POST /open-apis/drive/v1/permissions/<token>/members \
  --data '{"member_type":"openid","member_id":"ou_xxx","perm":"view"}'

# List permissions
lark-cli api GET /open-apis/drive/v1/permissions/<token>/members \
  --params '{"type":"docx"}'
```
