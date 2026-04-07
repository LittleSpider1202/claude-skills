---
name: task-graph
description: |
  项目任务进度可视化。运行脚本从 feature_list.json 生成彩色 DAG 依赖图。
  当用户说"查看项目进度"、"任务进度"、"进度图"、"task graph"、"依赖图"时触发。
allowed-tools:
  - Bash
---

# /task-graph — 项目任务进度 DAG

运行脚本，直接展示输出：

```bash
python3 ~/.claude/skills/task-graph/scripts/graph.py feature_list.json 2>/dev/null || python ~/.claude/skills/task-graph/scripts/graph.py feature_list.json
```

不做额外分析，直接展示脚本输出。
