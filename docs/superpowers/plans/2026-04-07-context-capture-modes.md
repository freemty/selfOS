# Context Capture Modes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement two zero-friction context capture modes — Chat Mode (Stop hook auto-ingest from conversations) and Interview Mode (`/wiki interview` for wiki-driven questioning).

**Architecture:** Chat Mode uses a Stop hook + Python extraction script that analyzes conversation text for personal context, then silently updates wiki pages. Interview Mode is a new skill command that scans wiki for gaps (Open Questions, thin pages, timeline holes, vague relationships) and generates targeted questions.

**Tech Stack:** Shell hooks (settings.json), Python scripts, Claude Code skill (markdown)

---

## File Structure

```
~/.claude/hooks/
  wiki-auto-ingest.sh            # Stop hook entry point

~/knowledge-base/
  scripts/
    auto-ingest.py               # Analyze conversation, decide what to ingest
    interview-questions.py       # Scan wiki for gaps, generate question candidates

~/.claude/skills/llm-wiki/
  SKILL.md                       # Add /wiki interview command
  references/
    interview-workflow.md         # Interview prompt reference
```

---

### Task 1: Chat Mode — Stop Hook Script

**Files:**
- Create: `~/.claude/hooks/wiki-auto-ingest.sh`
- Create: `~/knowledge-base/scripts/auto-ingest.py`

- [ ] **Step 1: Write the auto-ingest analysis script**

```python
#!/usr/bin/env python3
"""
Analyze a Claude Code conversation transcript for personal context worth ingesting.
Called by the Stop hook. Reads conversation from stdin or file.
Outputs: a markdown file in wiki/sources/ if valuable context found, else exits silently.
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path

KB_ROOT = Path(os.path.expanduser("~/knowledge-base"))

def extract_user_messages(conversation_text):
    """Extract lines that appear to be user messages from CC session output."""
    lines = conversation_text.strip().split('\n')
    user_parts = []
    for line in lines:
        # CC session format: user messages are typically after ❯ or > prompts
        # This is a heuristic — may need tuning
        if line.strip() and not line.startswith('  ') and not line.startswith('─'):
            user_parts.append(line)
    return '\n'.join(user_parts)

def has_personal_context(text):
    """Heuristic: does this text contain personal context worth capturing?"""
    personal_signals = [
        # Chinese personal context signals
        r'我觉得', r'我发现', r'我想', r'我的', r'让我',
        r'今天', r'昨天', r'最近', r'之前',
        r'感觉', r'有意思', r'震撼', r'反思',
        r'和.{1,4}聊', r'跟.{1,4}说',
        # English personal signals
        r'I think', r'I feel', r'I noticed', r'I realized',
        r'today', r'yesterday', r'recently',
    ]
    matches = sum(1 for p in personal_signals if re.search(p, text))
    # Need at least 2 signals to consider it personal context
    return matches >= 2

def save_session_source(user_text, full_text):
    """Save as a source page in wiki/sources/."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M")
    
    # Generate slug from first meaningful line
    first_line = user_text.split('\n')[0][:60].strip()
    slug = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', first_line.lower())
    slug = re.sub(r'[\s_]+', '-', slug).strip('-')[:40]
    if not slug:
        slug = f"session-{time_str}"
    
    filename = f"auto-{date_str}-{slug}.md"
    filepath = KB_ROOT / "wiki" / "sources" / filename
    
    if filepath.exists():
        return None  # Already captured
    
    page = f"""---
title: "CC session: {first_line[:60]}"
type: source
created: {date_str}
updated: {date_str}
sources: []
tags: [auto-captured, cc-session]
summary: "Auto-captured from Claude Code session"
source_type: "cc-session"
confidence: low
---

# CC Session — {date_str} {time_str}

{full_text[:5000]}
"""
    filepath.write_text(page, encoding='utf-8')
    
    # Append to log
    log_path = KB_ROOT / "wiki" / "log.md"
    if log_path.exists():
        with open(log_path, 'a') as f:
            f.write(f"\n## [{date_str}] auto-capture | CC session: {first_line[:40]}\n")
    
    return filepath

def main():
    # Read conversation text from environment or recent session
    # The Stop hook passes the session summary via stdin or env var
    text = sys.stdin.read() if not sys.stdin.isatty() else ""
    
    if not text:
        # Try to read from CC session file if available
        session_dir = Path(os.path.expanduser("~/.claude/projects"))
        # Fallback: no text available
        sys.exit(0)
    
    if len(text) < 100:
        sys.exit(0)  # Too short to be meaningful
    
    if not has_personal_context(text):
        sys.exit(0)  # No personal context detected
    
    user_text = extract_user_messages(text)
    result = save_session_source(user_text, text)
    
    if result:
        # Silent git commit
        os.system(f'cd {KB_ROOT} && git add wiki/sources/auto-* wiki/log.md && git commit -m "feat(wiki): auto-capture CC session" --quiet 2>/dev/null')

if __name__ == '__main__':
    main()
```

Write this to `~/knowledge-base/scripts/auto-ingest.py`.

- [ ] **Step 2: Write the Stop hook shell script**

```bash
#!/bin/bash
# wiki-auto-ingest.sh — Stop hook for auto-capturing CC sessions
# Called when Claude Code session ends

WIKI_ROOT="$HOME/knowledge-base"
SCRIPT="$WIKI_ROOT/scripts/auto-ingest.py"

# Only run if wiki exists
[ -d "$WIKI_ROOT/wiki" ] || exit 0
[ -f "$SCRIPT" ] || exit 0

# Pass conversation summary to the script
# The hook receives session context via environment
python3 "$SCRIPT" 2>/dev/null &
```

Write this to `~/.claude/hooks/wiki-auto-ingest.sh` and `chmod +x`.

- [ ] **Step 3: Register the Stop hook in settings.json**

Read `~/.claude/settings.json`, add to the `hooks` object:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "command": "bash ~/.claude/hooks/wiki-auto-ingest.sh"
      }
    ]
  }
}
```

Use the `update-config` skill or manual edit. Preserve existing hooks.

- [ ] **Step 4: Test the hook**

Start a new CC session, have a brief conversation with personal context ("我今天去跑步了，感觉最近状态不错"), then exit. Check:

```bash
ls ~/knowledge-base/wiki/sources/auto-*
# Should see a new auto-captured source page
```

- [ ] **Step 5: Commit**

```bash
cd ~/knowledge-base && git add scripts/auto-ingest.py && git commit -m "feat: add auto-ingest script for CC session capture"
```

---

### Task 2: Interview Mode — Gap Analysis Script

**Files:**
- Create: `~/knowledge-base/scripts/interview-questions.py`

- [ ] **Step 1: Write the gap analysis script**

```python
#!/usr/bin/env python3
"""
Scan wiki for context gaps and generate interview question candidates.
Outputs a ranked list of questions as JSON to stdout.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

KB_ROOT = Path(os.path.expanduser("~/knowledge-base"))
WIKI = KB_ROOT / "wiki"

def scan_open_questions():
    """Extract Open Questions from all concept pages."""
    questions = []
    for f in (WIKI / "concepts").glob("*.md"):
        content = f.read_text(encoding='utf-8')
        # Find ## Open Questions section
        oq_match = re.search(r'## Open Questions\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if oq_match:
            section = oq_match.group(1).strip()
            for line in section.split('\n'):
                line = line.strip().lstrip('- ')
                if line and len(line) > 10:
                    questions.append({
                        'type': 'open_question',
                        'source': f.stem,
                        'question': line,
                        'priority': 1
                    })
    return questions

def scan_thin_pages():
    """Find concept/entity pages with very little content."""
    questions = []
    for subdir in ['concepts', 'entities']:
        for f in (WIKI / subdir).glob("*.md"):
            content = f.read_text(encoding='utf-8')
            # Strip frontmatter
            body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
            word_count = len(body.split())
            if word_count < 100:
                title_match = re.search(r'title: "(.+?)"', content)
                title = title_match.group(1) if title_match else f.stem
                questions.append({
                    'type': 'thin_page',
                    'source': f.stem,
                    'question': f'Wiki 里关于"{title}"的记录很少（{word_count} 词）。你能多讲讲这个话题吗？',
                    'priority': 2
                })
    return questions

def scan_timeline_gaps():
    """Find months with very few source pages."""
    from collections import Counter
    month_counts = Counter()
    for f in (WIKI / "sources").glob("*.md"):
        # Extract date from filename
        date_match = re.match(r'(?:notion|cc|gem|auto)-(\d{4}-\d{2})', f.name)
        if date_match:
            month_counts[date_match.group(1)] += 1
    
    questions = []
    # Find months with < 5 entries (sparse)
    all_months = sorted(month_counts.keys())
    if all_months:
        for month in all_months:
            if month_counts[month] < 5:
                questions.append({
                    'type': 'timeline_gap',
                    'source': month,
                    'question': f'{month} 这个月的记录比较少（只有 {month_counts[month]} 条）。那段时间你在做什么？有什么特别的经历吗？',
                    'priority': 3
                })
    return questions

def scan_vague_entities():
    """Find entity pages with no Mentions or very short Connections."""
    questions = []
    for f in (WIKI / "entities").glob("*.md"):
        content = f.read_text(encoding='utf-8')
        title_match = re.search(r'title: "(.+?)"', content)
        title = title_match.group(1) if title_match else f.stem
        
        # Check if Mentions section is empty or missing
        mentions = re.search(r'## Mentions\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if not mentions or len(mentions.group(1).strip()) < 50:
            questions.append({
                'type': 'vague_entity',
                'source': f.stem,
                'question': f'你多次提到 {title}，但 wiki 里关于你们关系的描述不太详细。你们是怎么认识的？什么时候开始觉得 ta 对你很重要？',
                'priority': 2
            })
    return questions

def main():
    all_questions = []
    all_questions.extend(scan_open_questions())
    all_questions.extend(scan_thin_pages())
    all_questions.extend(scan_timeline_gaps())
    all_questions.extend(scan_vague_entities())
    
    # Sort by priority
    all_questions.sort(key=lambda q: q['priority'])
    
    # Output as JSON
    print(json.dumps(all_questions, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
```

Write to `~/knowledge-base/scripts/interview-questions.py`.

- [ ] **Step 2: Test the script**

```bash
cd ~/knowledge-base && python3 scripts/interview-questions.py | python3 -c "
import json, sys
qs = json.load(sys.stdin)
print(f'Total questions: {len(qs)}')
for q in qs[:5]:
    print(f'  [{q[\"type\"]}] {q[\"question\"][:80]}')
"
```

Expected: 20+ questions across 4 types.

- [ ] **Step 3: Commit**

```bash
cd ~/knowledge-base && git add scripts/interview-questions.py && git commit -m "feat: add interview question generator — scans wiki for context gaps"
```

---

### Task 3: Interview Mode — Skill Integration

**Files:**
- Modify: `~/.claude/skills/llm-wiki/SKILL.md`
- Create: `~/.claude/skills/llm-wiki/references/interview-workflow.md`

- [ ] **Step 1: Write the interview workflow reference**

```markdown
# Interview Workflow

You are conducting a "口述历史" (oral history) interview to fill context gaps in the LLM Wiki.

## Context
- Wiki root: {wiki_root}
- Questions generated by: `python3 scripts/interview-questions.py`

## Principles
1. **Ask one question at a time.** Never batch questions.
2. **Be conversational, not clinical.** "你能讲讲..." not "请描述..."
3. **Follow up naturally.** If the user's answer opens a new thread, follow it.
4. **Absorb silently.** After each answer, update the relevant wiki page without asking permission.
5. **Use wiki context in your questions.** Reference what you already know to make questions specific.

## Steps

### 1. Generate questions
Run: `python3 {wiki_root}/scripts/interview-questions.py`
Parse the JSON output. Select top 3 questions by priority.

### 2. Set the tone
Start with something like:
> "我看了一下 wiki 的状态，有几个地方我很好奇想问你。就像聊天一样，随便说就好。"

### 3. Ask first question
Pick the highest-priority question. Frame it conversationally using wiki context.

BAD: "Wiki 中关于'家庭与成长'的记录内容不足，请补充。"
GOOD: "wiki 里你提到过'每周和父母至少沟通一次 → 我还是太幼稚太任性了'，但后来没有更多关于你和家人关系的记录了。你们现在的沟通是什么状态？"

### 4. Absorb answer
After user responds:
- Update relevant concept page (add to ## Evolution or ## Key Insights)
- Update relevant entity page (add to ## Mentions)
- If answer reveals a new concept, create a stub page
- Commit silently

### 5. Follow up or next question
If the answer naturally leads somewhere, follow it (this is Mode 1 chat blending in).
Otherwise, ask the next question.

### 6. Close
After 3-5 questions (or when user seems done):
> "今天就聊到这里。Wiki 已经更新了 X 个页面。下次有新的问题我再来找你。"
Commit all changes.
```

Write to `~/.claude/skills/llm-wiki/references/interview-workflow.md`.

- [ ] **Step 2: Add /wiki interview to SKILL.md**

Append after the `/wiki compile` section in SKILL.md:

```markdown
### `/wiki interview`

Oral history mode — wiki asks you questions to fill context gaps.

1. Run `python3 {wiki_root}/scripts/interview-questions.py` to get question candidates
2. Read the skill's `references/interview-workflow.md` for the full prompt
3. Select top 3 questions by priority
4. Ask questions one at a time, conversationally
5. After each answer, silently update relevant wiki pages
6. Follow up naturally — if user opens a new thread, follow it
7. After 3-5 questions, summarize what was updated and commit
```

- [ ] **Step 3: Commit**

```bash
git -C ~/.claude/skills/llm-wiki add -A 2>/dev/null
cd ~/knowledge-base && git add -A && git commit -m "feat(wiki): add /wiki interview command — oral history gap filling"
```

---

### Task 4: Register Stop Hook in Settings

**Files:**
- Modify: `~/.claude/settings.json`

- [ ] **Step 1: Add Stop hook to settings.json**

Use the Skill tool to invoke `update-config`, or manually read+edit `~/.claude/settings.json`:

Add to the `hooks` object:

```json
"Stop": [
  {
    "matcher": "",
    "command": "bash ~/.claude/hooks/wiki-auto-ingest.sh"
  }
]
```

Preserve all existing hooks (Notification, PreToolUse, PostToolUse, etc.).

- [ ] **Step 2: Verify hook registration**

```bash
cat ~/.claude/settings.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
hooks = d.get('hooks', {})
stop = hooks.get('Stop', [])
print(f'Stop hooks: {len(stop)}')
for h in stop:
    print(f'  {h.get(\"command\", \"?\")[:60]}')
"
```

Expected: `Stop hooks: 1` with `bash ~/.claude/hooks/wiki-auto-ingest.sh`.

- [ ] **Step 3: Commit hook script**

```bash
# Hook script is outside the wiki repo, just verify it exists
ls -la ~/.claude/hooks/wiki-auto-ingest.sh
```

---

### Task 5: Update CLAUDE.md and Documentation

**Files:**
- Modify: `~/knowledge-base/CLAUDE.md`
- Modify: `~/knowledge-base/TODO.md`

- [ ] **Step 1: Add new commands to CLAUDE.md Quick commands table**

Add to the Wiki Operations table:

```markdown
| `/wiki interview` | 口述历史模式：wiki 主动提问填补 context gap | `/wiki interview` |
```

Add a new section after Wiki Operations:

```markdown
### Auto-Capture (Chat Mode)

每次 Claude Code 对话结束时，Stop hook 自动检测对话中的个人 context，有价值的内容静默保存为 `wiki/sources/auto-*.md`。你不需要做任何事情。
```

- [ ] **Step 2: Update TODO.md — mark completed**

Mark "设计 Stop hook 让 CC 对话自动沉淀进 wiki" as done.

- [ ] **Step 3: Commit**

```bash
cd ~/knowledge-base && git add CLAUDE.md TODO.md && git commit -m "docs: add /wiki interview and auto-capture to CLAUDE.md"
```
