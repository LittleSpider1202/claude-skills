---
name: yt-search
description: Search YouTube videos by keyword, extract metadata (title, views, channel, duration), download subtitles/transcripts, and get video descriptions. Powered by yt-dlp. Activates on intent like "search YouTube for X", "find YouTube videos about X", "get transcript from YouTube".
---

# YouTube Search & Extract

Search YouTube for videos by keyword, extract metadata, download subtitles/transcripts, and get video descriptions. All powered by yt-dlp.

## Prerequisites

- `yt-dlp` installed: `pip install -U yt-dlp`
- Node.js installed (for YouTube JS challenge solving)
- YouTube cookies file for authenticated access

### Cookies Setup

YouTube requires cookies to avoid bot detection. Export cookies from your browser:

1. Install browser extension "Get cookies.txt LOCALLY"
2. Visit youtube.com (logged in)
3. Export cookies to a known path

## Configuration

Before running any command, determine these paths from the user's environment:

| Variable | Description | How to find |
|----------|-------------|-------------|
| `COOKIES` | Path to YouTube cookies.txt | Ask user or check common locations |
| `NODE_PATH` | Path to node.exe | `where node` or `which node` |

The standard yt-dlp base command is:

```bash
yt-dlp --js-runtimes "node:NODE_PATH" --remote-components ejs:github --cookies COOKIES
```

Replace `NODE_PATH` and `COOKIES` with actual paths.

## When This Skill Activates

**Explicit:** User says "/yt-search", "search YouTube", "find videos on YouTube"

**Intent detection:** Recognize requests like:
- "Search YouTube for [topic]"
- "Find YouTube videos about [topic]"
- "Get the transcript/subtitles from this YouTube video"
- "What are the top videos about [topic]"
- "Download captions from [YouTube URL]"
- "Get the description of this YouTube video"

## Commands

### 1. Search Videos by Keyword

Search YouTube and return top N results with metadata.

```bash
yt-dlp --js-runtimes "node:NODE_PATH" --remote-components ejs:github --cookies COOKIES \
  "ytsearchN:QUERY" --dump-json --flat-playlist 2>/dev/null
```

- Replace `N` with number of results (default: 10)
- Replace `QUERY` with search keywords

**Parse output** (one JSON object per line):

| Field | Description |
|-------|-------------|
| `id` | Video ID |
| `title` | Video title |
| `url` | Video URL (`https://www.youtube.com/watch?v=ID`) |
| `duration` | Duration in seconds |
| `view_count` | Number of views |
| `channel` | Channel name |
| `upload_date` | Upload date (may be null in flat playlist) |

**Display format:** Present results as a numbered table:

```
| # | Title | Channel | Views | Duration | URL |
```

Sort by view_count descending by default unless user specifies otherwise.

### 2. Get Video Metadata & Description

Get full metadata including description/copytext for a single video.

```bash
yt-dlp --js-runtimes "node:NODE_PATH" --remote-components ejs:github --cookies COOKIES \
  --skip-download --dump-json "VIDEO_URL" 2>/dev/null
```

**Key fields to extract:**

| Field | Description |
|-------|-------------|
| `title` | Video title |
| `description` | Full video description (the copytext) |
| `channel` | Channel name |
| `upload_date` | Upload date (YYYYMMDD) |
| `duration` | Duration in seconds |
| `view_count` | Views |
| `like_count` | Likes |
| `comment_count` | Comments |
| `tags` | Video tags |
| `categories` | Video categories |

### 3. Download Subtitles/Transcript

Download auto-generated or manual subtitles.

```bash
yt-dlp --js-runtimes "node:NODE_PATH" --remote-components ejs:github --cookies COOKIES \
  --write-subs --write-auto-subs --sub-langs "LANGS" --skip-download \
  -o "OUTPUT_DIR/%(title)s.%(ext)s" "VIDEO_URL" 2>/dev/null
```

- `LANGS`: Comma-separated language codes, e.g. `en,zh-Hans`
- Common codes: `en` (English), `zh-Hans` (Simplified Chinese), `zh-Hant` (Traditional Chinese), `ja` (Japanese), `ko` (Korean)
- Output: `.vtt` subtitle files

**To extract clean text from VTT:** After downloading, strip timestamps and tags to get plain transcript. Use Python:

```python
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('subtitle.vtt', 'r', encoding='utf-8') as f:
    content = f.read()
content = re.sub(r'WEBVTT.*?\n\n', '', content, flags=re.DOTALL)
content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', content)
content = re.sub(r'<[^>]+>', '', content)
lines = []
prev = ''
for line in content.split('\n'):
    line = line.strip()
    if line and line != prev:
        lines.append(line)
        prev = line
text = ' '.join(lines)
text = re.sub(r'\s+', ' ', text).strip()
print(text)
```

### 4. List Available Subtitles

Check what subtitle languages are available for a video.

```bash
yt-dlp --js-runtimes "node:NODE_PATH" --remote-components ejs:github --cookies COOKIES \
  --list-subs "VIDEO_URL" 2>/dev/null
```

### 5. Download Audio Only

Extract audio from a video (useful for podcast-style content).

```bash
yt-dlp --js-runtimes "node:NODE_PATH" --remote-components ejs:github --cookies COOKIES \
  -x --audio-format mp3 -o "OUTPUT_DIR/%(title)s.%(ext)s" "VIDEO_URL"
```

## Autonomy Rules

**Run automatically (no confirmation):**
- Search queries (`ytsearchN:`)
- Metadata extraction (`--dump-json`)
- List subtitles (`--list-subs`)

**Ask before running:**
- Download subtitles (writes files)
- Download audio (writes files, may be large)
- Any batch operation on multiple videos

## Common Workflows

### Research a Topic

1. Search: `ytsearch10:TOPIC` to find top videos
2. Present results as table, let user pick
3. Extract descriptions and transcripts from selected videos
4. Optionally push to NotebookLM for deep analysis

### Extract Video Copytext

1. Get metadata with `--dump-json`
2. Extract `title`, `description`, `tags`
3. Download subtitles if transcript needed
4. Clean VTT to plain text

### Batch Research (with NotebookLM)

1. Search YouTube for topic
2. User selects videos
3. Add selected YouTube URLs to NotebookLM: `notebooklm source add "URL"`
4. NotebookLM auto-extracts captions and builds knowledge base
5. Generate reports, podcasts, quizzes from the knowledge base

## Output Encoding

On Windows, always set UTF-8 encoding when processing output with Python:

```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| "Sign in to confirm you're not a bot" | Missing or expired cookies | Re-export cookies from browser |
| "No supported JavaScript runtime" | Node.js not configured | Add `--js-runtimes "node:PATH"` |
| JS challenge solver warning | Missing remote components | Add `--remote-components ejs:github` |
| Timeout | Network or proxy issue | Check proxy settings, retry |

## Environment Notes

- Python path: Detect with `where python` or use full path
- Node path: Detect with `where node` or use full path
- Proxy: Do NOT bypass proxy (`--proxy ""`) unless user requests it — YouTube may require proxy in some regions
