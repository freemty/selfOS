# 录音转写 → Wiki 归档 Runbook

> Meeting 录音一键转写并编译进 wiki 的完整操作流程

## Problem
Meeting 录音需要转文字、提取关键信息、归档到 wiki source page，手动做太慢。

## Cause
建立了 `/transcribe` skill + `scripts/transcribe.py` 脚本自动化此流程。

## Solution

### 完整流程

```
录音文件 → ASR 转写 → raw/ 保存原文 → 提取要点 → wiki/sources/ 归档 → index/log 更新
```

### Step 1: 转写

```bash
/transcribe <file_path>
# 或手动:
python3 ~/selfOS/scripts/transcribe.py recording.mp3 -o /tmp/transcript.md
```

### Step 2: 保存原文到 raw/

```bash
cp /tmp/transcript.md ~/selfOS/raw/meeting-YYYY-MM-DD-<slug>-transcript.md
```

命名规则: `meeting-{date}-{描述slug}-transcript.md`

### Step 3: 编译为 Wiki Source

创建 `wiki/sources/cc-YYYY-MM-DD-<slug>.md`：
- YAML frontmatter (title, type: source, tags, summary, source_type: "audio-transcript")
- Context 段（谁、什么时间、为什么）
- Key Points / Decisions 段（从转写中提取）
- Action Items 段
- 引用原文关键句（不需要全文）

### Step 4: Speaker Mapping

如果知道说话人身份，替换 `Speaker 1/2/3` 为真名。

### Step 5: 更新 Index + Log

- `wiki/index.md` 加 source 入口
- `wiki/log.md` 追加操作记录
- Cross-link 到相关 entity/concept pages

## Commands
```bash
# 一步到位（skill 自动处理全流程）
/transcribe /path/to/meeting.mp3

# 手动分步
python3 ~/selfOS/scripts/transcribe.py meeting.mp3 -o /tmp/t.md
cp /tmp/t.md ~/selfOS/raw/meeting-2026-05-18-hao-1on1-transcript.md
# 然后手动编译 wiki source page
```

## Notes
- Date: 2026-05-18
- 首次使用需设置 `VOLCENGINE_ASR_API_KEY`（见 toolchain/volcengine-asr.md）
- WeChat 录音文件常见路径: `~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/*/temp/drag/`
- 说话人分离质量取决于音频质量（多人同时说话时准确度下降）
