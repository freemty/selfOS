# selfOS Skill Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete selfOS skill suite with `/digest`, upgraded `/interview` (3 question pools), preference tagging in auto-capture, and clean fork-ready distribution.

**Architecture:** 4 phases — (1) `/digest` skill, (2) `/interview` upgrade with `pending_questions` support, (3) preference tagging in `auto-ingest.py`, (4) distribution packaging (`setup.sh`, hook relocation, CLAUDE.md updates). Phase 1 and 2 are independent and can run in parallel.

**Tech Stack:** Claude Code skills (markdown), Python 3 scripts, bash, git

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `.claude/skills/digest/skill.md` | `/digest` skill definition |
| Modify | `.claude/skills/selfos-completion/skill.md` | Add `pending_questions` pool to `/interview` |
| Modify | `.claude/skills/selfos-completion/references/interview-workflow.md` | Update interview workflow for new question types |
| Modify | `scripts/interview-questions.py` | Add `scan_pending_questions()` as priority 0 |
| Modify | `scripts/auto-ingest.py` | Add preference detection + `pending_questions` writing |
| Create | `hooks/auto-capture.sh` | Repo-local copy of auto-capture hook |
| Create | `setup.sh` | One-command install for fork users |
| Modify | `CLAUDE.md` | Add `/digest` docs, update command table |

---

### Task 1: Create `/digest` skill

**Files:**
- Create: `.claude/skills/digest/skill.md`

- [ ] **Step 1: Create digest skill directory**

```bash
mkdir -p .claude/skills/digest
```

- [ ] **Step 2: Write the skill file**

Create `.claude/skills/digest/skill.md`:

```markdown
---
name: digest
description: "Wiki activity digest — daily/weekly review of changes plus recommended questions. Triggers: /digest, wiki recap, 回顾, what changed."
user-invocable: true
---

# /digest — Wiki Activity Digest

Review what changed in your wiki and get a recommended question to deepen your knowledge base.

## When to Use

- User says `/digest`, `/digest week`, or `/digest question`
- User wants to see wiki activity or get a daily prompt

**Not for:** querying wiki content (`/wiki query`), active interview (`/interview`), thought capture (`/thought`)

## Commands

| Command | What it does |
|---------|-------------|
| `/digest` | Today's wiki changes + 1 recommended question |
| `/digest week` | This week's changes + top 3 active concepts + 2-3 questions |
| `/digest question` | Just a recommended question, no recap |

## Daily Digest Flow

### 1. Gather changes

Run these commands to collect today's wiki activity:

```bash
# Git changes in wiki/ today
git log --since="midnight" --name-status --pretty=format:"%h %s" -- wiki/

# If no changes today, fall back to last 3 days
git log --since="3 days ago" --name-status --pretty=format:"%h %s" -- wiki/
```

Also read the last 10 entries from `wiki/log.md`.

### 2. Categorize changes

Group into:
- **New pages**: files with status `A` (added)
- **Updated pages**: files with status `M` (modified)
- **New connections**: grep added lines for `[[` wikilinks in modified files

For each changed file, read its frontmatter to get title and type.

### 3. Pick a recommended question

Run: `python3 scripts/interview-questions.py`

Pick the highest-priority question. If there are `pending_questions` type entries (priority 0), prefer those — they connect to the user's recent thinking.

Frame the question with reference to today's changes when possible:
- GOOD: "你今天写了关于 X 的想法，wiki 里 [[concepts/Y]] 有个相关的 open question：..."
- BAD: "这是一个推荐问题：..."

### 4. Present

```markdown
### 📊 Wiki 动态 (YYYY-MM-DD)

**新增 (N)**
- [[sources/thought-2026-04-09-xxx]] — 快速想法
- [[concepts/xxx]] — 新概念

**更新 (N)**
- [[concepts/ai4ai]] — 新增 Context Recovery 段落

**新建连接**
- [[concepts/taste与ambition]] ↔ [[concepts/科研路线选择]]

---

**推荐问题**
> [基于 context 的具体问题]
```

### 5. Transition to interview

If user answers the recommended question, switch to interview mode:
- Absorb the answer silently (update relevant wiki pages)
- Follow up naturally if the answer opens a thread
- After 1-2 follow-ups, close or ask "还要再来一个问题吗？"

## Weekly Digest Flow

Same as daily, but:
- `git log --since="1 week ago"` for changes
- Add **Top 3 active concepts** (most frequently modified/referenced this week)
- Add **Timeline coverage** change ("本周新覆盖了 2025-10 的 N 条记录")
- 2-3 recommended questions instead of 1

## Common Mistakes

- Showing raw git diff output instead of human-readable summaries
- Recommending a question with no connection to recent activity
- Not reading the changed files to understand what actually changed (just showing filenames is lazy)
```

- [ ] **Step 3: Create global symlink**

```bash
ln -sf "$(pwd)/.claude/skills/digest" ~/.claude/skills/digest
```

- [ ] **Step 4: Verify skill loads**

Open a new CC session in the selfOS directory and run `/digest` — confirm the skill is recognized and triggers correctly. It should read `wiki/log.md` and run `git log`.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/digest/skill.md
git commit -m "feat: add /digest skill — wiki activity review + recommended questions"
```

---

### Task 2: Upgrade `interview-questions.py` with `pending_questions` support

**Files:**
- Modify: `scripts/interview-questions.py:83-224`

- [ ] **Step 1: Add `scan_pending_questions` function**

Add this new scanner function after the existing imports and helpers (after line 76), before the existing `scan_open_questions`:

```python
def scan_pending_questions(questions: list[dict]) -> None:
    """Priority 0: Pending questions from auto-captured sessions.

    Scans all wiki/sources/ pages for a `pending_questions` YAML field
    in frontmatter. These are questions generated by the preference
    tagging system in auto-ingest.py.
    """
    sources_dir = WIKI_ROOT / "sources"
    if not sources_dir.is_dir():
        return

    pq_re = re.compile(r'^pending_questions:\s*$', re.MULTILINE)
    item_re = re.compile(r'^\s+-\s+"(.+?)"', re.MULTILINE)

    for path in sorted(sources_dir.glob("*.md")):
        text = _read_file(path)
        if text is None:
            continue

        fm, _ = _strip_frontmatter(text)
        if not pq_re.search(fm):
            continue

        for m in item_re.finditer(fm):
            question_text = m.group(1)
            questions.append({
                "type": "pending_question",
                "source": path.stem,
                "source_path": str(path.relative_to(WIKI_ROOT)),
                "question": question_text,
                "priority": 0,
            })
```

- [ ] **Step 2: Register the new scanner in `main()`**

Change the `main()` function to call `scan_pending_questions` first:

```python
def main() -> None:
    questions: list[dict] = []

    scan_pending_questions(questions)
    scan_open_questions(questions)
    scan_thin_pages(questions)
    scan_timeline_gaps(questions)
    scan_vague_entities(questions)

    # Stable sort by priority (ascending — 0 = highest priority)
    questions.sort(key=lambda q: q["priority"])

    json.dump(questions, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
```

- [ ] **Step 3: Test manually**

Create a temporary test file to verify scanning works:

```bash
cat > /tmp/test-pending.md << 'EOF'
---
title: "test"
type: source
created: 2026-04-09
updated: 2026-04-09
sources: []
tags: [auto-captured]
summary: "test"
source_type: "cc-session"
pending_questions:
  - "你说'X比Y好'——具体指什么场景？"
  - "你提到Z方向，基于什么判断？"
---

# test
EOF

# Temporarily copy to wiki/sources/, run script, then clean up
cp /tmp/test-pending.md wiki/sources/_test-pending.md
python3 scripts/interview-questions.py | python3 -m json.tool | head -20
rm wiki/sources/_test-pending.md
```

Expected: JSON output should contain 2 entries with `"type": "pending_question"` and `"priority": 0` at the top.

- [ ] **Step 4: Commit**

```bash
git add scripts/interview-questions.py
git commit -m "feat: add pending_questions scanning to interview-questions.py (priority 0)"
```

---

### Task 3: Update selfos-completion skill for upgraded `/interview`

**Files:**
- Modify: `.claude/skills/selfos-completion/skill.md`
- Modify: `.claude/skills/selfos-completion/references/interview-workflow.md`

- [ ] **Step 1: Update the Interview Mode section in skill.md**

In `.claude/skills/selfos-completion/skill.md`, replace the current Interview Mode section (lines 88-94) with:

```markdown
## Interview Mode

Run `python3 {wiki_root}/scripts/interview-questions.py` → JSON with prioritized gaps:

| Priority | Type | Source |
|----------|------|--------|
| 0 | Pending Questions | Auto-Capture 标记的未展开偏好/判断（`pending_questions` frontmatter） |
| 1 | Open Questions | 概念页底部的 Open Questions |
| 2 | Thin Pages | 概念/实体页 < 100 词 |
| 2 | Vague Entities | 实体页 Mentions 为空或过短 |
| 3 | Timeline Gaps | 月源少于 5 条 |

**Conduct:** Read `references/interview-workflow.md` for full behavioral guide. Key rules:
- One question at a time, conversational tone
- Reference existing wiki content to make questions specific
- **Silently update** relevant wiki pages after each answer
- For `pending_question` type: after absorbing the answer, **remove that question from the source file's `pending_questions` frontmatter list**. If the list becomes empty, remove the `pending_questions` field entirely.
- 3-5 questions per session, then commit
```

- [ ] **Step 2: Update interview-workflow.md for pending_questions handling**

In `.claude/skills/selfos-completion/references/interview-workflow.md`, add a new section after "### 4. Absorb answer" (after line 37):

```markdown
### 4b. Handle pending_questions cleanup

If the question came from a `pending_question` type (check the JSON `source_path` field):

1. Read the source file at `wiki/{source_path}`
2. Find the specific question text in the `pending_questions` YAML list
3. Remove that one line from the list
4. If no questions remain, remove the entire `pending_questions:` block from frontmatter
5. Save the file

Example — before:
```yaml
pending_questions:
  - "你说'X比Y好'——具体指什么场景？"
  - "你提到Z方向，基于什么判断？"
```

After answering the first question:
```yaml
pending_questions:
  - "你提到Z方向，基于什么判断？"
```

After answering both — remove the field entirely (no empty list).
```

- [ ] **Step 3: Update the mode table in skill.md**

In `.claude/skills/selfos-completion/skill.md`, update the Modes table (line 21-26) to reflect the upgraded interview:

```markdown
| Command | Pool | What it picks |
|---------|------|---------------|
| `/bookmark-chat` | Twitter bookmarks | Bookmarked tweets missing "why I saved this" |
| `/complete` or `/bookmark-chat thoughts` | Notion Thoughts | One-line thoughts missing context |
| `/interview` | Wiki gaps + pending questions | Pending偏好追问 → Open Questions → Thin pages → Timeline gaps |
| (no args) | Mixed bookmarks + thoughts | Random from either pool |
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/selfos-completion/skill.md .claude/skills/selfos-completion/references/interview-workflow.md
git commit -m "feat: upgrade /interview with 3-pool question system (pending + open + gaps)"
```

---

### Task 4: Add preference tagging to `auto-ingest.py`

**Files:**
- Modify: `scripts/auto-ingest.py`

- [ ] **Step 1: Add preference signal patterns**

After the existing `PERSONAL_SIGNALS_EN` list (after line 63), add:

```python
# Preference / judgment signals for pending_questions generation
# These indicate unexpanded opinions, preferences, or reactions
PREFERENCE_SIGNALS = [
    # Unexpanded judgments
    (r"我觉得(.{5,40}?)(?:比|不如|好于|强于)", "judgment",
     "你说'{match}'——具体指什么场景下？基于什么判断？"),
    (r"(.{3,30}?)(?:不行|没前途|没戏|废了)", "judgment",
     "你提到'{match}'——是基于什么观察？在什么条件下？"),

    # Vague ideas
    (r"(?:我在想|我想|感觉)(.{5,50}?)(?:会不会|是不是|可能)", "vague_idea",
     "你说'{match}'——能展开说说吗？具体怎么关联的？"),
    (r"感觉(.{5,40}?)(?:和|跟)(.{3,20}?)有关系", "vague_idea",
     "你觉得'{g1}'和'{g2}'有关——具体怎么关联？"),

    # Emotional reactions
    (r"(?:被|让)(.{3,30}?)(?:震撼|震惊|感动|启发)", "emotional",
     "你说被'{match}'震撼——具体是什么触动了你？"),
    (r"(.{3,30}?)(?:太爽了|太牛了|太强了|太厉害)", "emotional",
     "你说'{match}'——具体是哪个点让你这么觉得？"),

    # Unexpanded preferences
    (r"(?:我比较倾向|我偏向|我更喜欢)(.{5,40})", "preference",
     "你说倾向'{match}'——基于什么考虑？"),
    (r"(?:以后|之后|未来)(?:可能会|打算|想)(.{5,40})", "preference",
     "你提到未来可能'{match}'——目前是什么推动了这个想法？"),
]
```

- [ ] **Step 2: Add `extract_pending_questions` function**

Add after the `generate_slug` function (after line 174):

```python
def extract_pending_questions(text):
    """Extract pending questions from preference/judgment signals in text.

    Returns a list of question strings, or empty list if none found.
    Keeps only user messages for scanning (lines starting with [User]).
    """
    # Only scan user messages
    user_lines = []
    for line in text.split("\n"):
        if line.startswith("[User]"):
            user_lines.append(line[6:].strip())
    user_text = "\n".join(user_lines)

    if not user_text:
        return []

    questions = []
    seen = set()

    for pattern, _signal_type, template in PREFERENCE_SIGNALS:
        for m in re.finditer(pattern, user_text):
            # Build question from template
            match_text = m.group(1).strip() if m.lastindex >= 1 else ""
            if not match_text or match_text in seen:
                continue
            seen.add(match_text)

            question = template.replace("{match}", match_text)
            if m.lastindex and m.lastindex >= 2:
                question = question.replace("{g1}", m.group(1).strip())
                question = question.replace("{g2}", m.group(2).strip())

            questions.append(question)

    # Cap at 3 questions per session to avoid noise
    return questions[:3]
```

- [ ] **Step 3: Update `build_frontmatter` to accept pending_questions**

Replace the existing `build_frontmatter` function (lines 177-189):

```python
def build_frontmatter(title, date_str, pending_questions=None):
    """Build YAML frontmatter for the source page."""
    lines = [
        '---',
        f'title: "{title}"',
        'type: source',
        f'created: {date_str}',
        f'updated: {date_str}',
        'sources: []',
        'tags: [auto-captured, cc-session]',
        'summary: "Auto-captured from Claude Code session"',
        'source_type: "cc-session"',
        'confidence: low',
    ]
    if pending_questions:
        lines.append('pending_questions:')
        for q in pending_questions:
            safe_q = q.replace('"', '\\"')
            lines.append(f'  - "{safe_q}"')
    lines.append('---')
    return '\n'.join(lines)
```

- [ ] **Step 4: Update `save_source` to pass pending_questions**

Replace the existing `save_source` function (lines 192-218):

```python
def save_source(text, date_str, slug):
    """Save conversation as a wiki source page. Returns filepath or None."""
    time_str = datetime.now().strftime("%H%M")
    filename = f"auto-{date_str}-{time_str}-{slug}.md"
    filepath = SOURCES_DIR / filename

    # Idempotency: skip if file already exists
    if filepath.exists():
        return None

    # Extract pending questions before truncating
    pending_qs = extract_pending_questions(text)

    # Truncate to max chars
    truncated = text[:MAX_CHARS]
    if len(text) > MAX_CHARS:
        truncated += "\n\n(truncated at 10000 chars)"

    # Build title from slug
    title = slug.replace("-", " ")

    frontmatter = build_frontmatter(title, date_str, pending_qs)
    content = f"""{frontmatter}

# {title}

## Session Content

{truncated}
"""

    filepath.write_text(content, encoding="utf-8")
    return filepath
```

- [ ] **Step 5: Test manually**

```bash
echo '[User] 我觉得agent scaling比RL scaling有前途多了，以后可能会all-in agent方向' | python3 -c "
import sys
sys.path.insert(0, 'scripts')
from auto_ingest import extract_pending_questions
text = sys.stdin.read()
qs = extract_pending_questions(text)
for q in qs:
    print(q)
"
```

Expected: Should output 1-2 questions like:
- "你说'agent scaling比RL scaling'——具体指什么场景下？基于什么判断？"
- "你提到未来可能'all-in agent方向'——目前是什么推动了这个想法？"

Note: The import path uses underscore (`auto_ingest`) because Python module imports convert hyphens. If the import fails, test by running directly:

```bash
echo '[User] 我觉得agent scaling比RL scaling有前途多了' | python3 scripts/auto-ingest.py
```

Then check the latest `wiki/sources/auto-*.md` for `pending_questions` in frontmatter.

- [ ] **Step 6: Commit**

```bash
git add scripts/auto-ingest.py
git commit -m "feat: add preference tagging to auto-ingest — generates pending_questions"
```

---

### Task 5: Distribution packaging

**Files:**
- Create: `hooks/auto-capture.sh`
- Create: `setup.sh`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Copy hook into repo**

Create `hooks/auto-capture.sh` — a repo-local version of the auto-capture hook that resolves paths relative to the script location:

```bash
#!/bin/bash
# Wiki Auto-Capture Hook (Stop)
# Pipes Claude Code session transcript to auto-ingest.py for wiki capture.
# Runs in background to avoid blocking Claude Code exit.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SELFOS_DIR="$(dirname "$SCRIPT_DIR")"
SCRIPT="$SELFOS_DIR/scripts/auto-ingest.py"

# Guard: script must exist
[ -f "$SCRIPT" ] || exit 0

# Read stdin (Stop hook JSON) and pipe to auto-ingest in background
INPUT=$(cat)
echo "$INPUT" | python3 "$SCRIPT" 2>/dev/null &

exit 0
```

```bash
mkdir -p hooks
# Write the file, then:
chmod +x hooks/auto-capture.sh
```

- [ ] **Step 2: Create setup.sh**

Create `setup.sh` at repo root:

```bash
#!/bin/bash
set -e

SELFOS_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo "selfOS Setup"
echo "============"
echo ""

# Ensure ~/.claude/skills exists
mkdir -p "$SKILLS_DIR"

# 1. Global skill symlinks
echo "Registering global skill symlinks..."
for skill in selfos selfos-completion thought digest; do
  target="$SELFOS_DIR/.claude/skills/$skill"
  link="$SKILLS_DIR/$skill"
  if [ ! -d "$target" ]; then
    echo "  skip $skill (not found in repo)"
    continue
  fi
  if [ -L "$link" ] || [ -d "$link" ]; then
    echo "  skip $skill (already exists)"
  else
    ln -s "$target" "$link"
    echo "  + $skill"
  fi
done

# 2. Auto-Capture hook (optional)
echo ""
echo "Auto-Capture hook registers a Stop hook that silently captures"
echo "personal context from Claude Code sessions into your wiki."
echo ""
read -p "Register Auto-Capture hook? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo ""
  echo "Add this to ~/.claude/settings.json under \"Stop\" hooks:"
  echo ""
  echo "  {"
  echo "    \"hooks\": [{"
  echo "      \"command\": \"bash $SELFOS_DIR/hooks/auto-capture.sh\","
  echo "      \"type\": \"command\""
  echo "    }],"
  echo "    \"matcher\": \"\""
  echo "  }"
  echo ""
fi

echo ""
echo "Done. Run '/wiki init' in Claude Code to initialize your wiki."
echo "Then try '/thought your first idea' to get started."
```

```bash
chmod +x setup.sh
```

- [ ] **Step 3: Update CLAUDE.md with `/digest` documentation**

In `CLAUDE.md`, add the `/digest` entry to the Quick commands section, after the Quick Thought Capture section and before the selfOS Completion section:

```markdown
### Wiki Digest

Skill: `.claude/skills/digest/` → symlink at `~/.claude/skills/digest`

| Command | Purpose | Example |
|---------|---------|---------|
| `/digest` | 今日 wiki 变化回顾 + 推荐问题 | `/digest` |
| `/digest week` | 本周回顾 + 活跃概念 + 推荐问题 | `/digest week` |
| `/digest question` | 只给推荐问题 | `/digest question` |
```

- [ ] **Step 4: Update CLAUDE.md quick command table summary**

Update the user mental model at the top of the Quick commands section. After the `### Wiki Operations` table, before `### Quick Thought Capture`, add:

```markdown
用户心智模型：`/thought` 记想法 → `/interview` 让 wiki 问我 → `/digest` 回顾变化 → `/wiki` 管理
```

- [ ] **Step 5: Commit everything**

```bash
git add hooks/auto-capture.sh setup.sh CLAUDE.md
git commit -m "feat: distribution packaging — setup.sh, repo-local hook, CLAUDE.md updates"
```

---

### Task 6: Integration test

- [ ] **Step 1: Test full flow end-to-end**

In a fresh CC session in the selfOS directory, run through the complete cycle:

```
1. /thought 我觉得selfOS最终会变成一个AI-native的日记系统
2. (回答 interview 问题)
3. /digest
4. /interview
5. (verify pending_questions are picked up if any exist)
```

Check:
- `wiki/sources/thought-2026-04-09-*.md` was created with frontmatter
- `wiki/index.md` was updated
- `/digest` shows today's changes
- `/interview` picks up pending_questions first (if auto-capture ran)

- [ ] **Step 2: Test setup.sh on clean state**

```bash
# Simulate what a fork user would see
ls -la ~/.claude/skills/digest  # Should be a symlink to this repo
cat setup.sh                     # Verify paths are relative
```

- [ ] **Step 3: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: integration test fixes"
```
