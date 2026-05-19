---
name: transcribe
description: "Use when user provides an audio file path (.mp3/.wav/.m4a/.aac) or says 转写/录音转文字/帮我转写. Also triggers on meeting recordings, voice memos, or any speech-to-text request."
user-invocable: true
---

# /transcribe — Audio Transcription + Wiki Ingest

Transcribe audio files using Volcengine (火山引擎) ASR API, then optionally compile the transcript into wiki as a source page.

## Wiki Root

**Always resolve to `~/selfOS/` (absolute: `/Users/sum_young/selfOS/`).** All paths relative to this root.

## When to Use

- User says `/transcribe <path>` or drops an audio file
- User says "转写", "录音转文字", "帮我转写"
- User provides audio file path (mp3/wav/m4a/aac/ogg)

**Not for:** live streaming ASR, TTS (text-to-speech), video transcription

## Prerequisites

- Environment variable: `VOLCENGINE_ASR_API_KEY`
- Script: `scripts/transcribe.py`
- Python package: `requests`

## Setup Guide (if API key missing)

If `VOLCENGINE_ASR_API_KEY` is not set, output the following setup instructions and STOP:

```
### 🔑 火山引擎 ASR 设置

1. 打开 https://console.volcengine.com/speech/app
2. 注册/登录（支持手机号）
3. 点击「语音识别」→「大模型语音识别」→「立即试用」（20 小时免费）
4. 在控制台创建 API Key
5. 设置环境变量：

   echo 'export VOLCENGINE_ASR_API_KEY="你的key"' >> ~/.zshrc
   source ~/.zshrc

设置好后再次运行 /transcribe 即可。
```

Do NOT attempt to transcribe without the key. Do NOT proceed with other steps.

## Flow

### 0. Check API Key

```bash
echo "${VOLCENGINE_ASR_API_KEY:-NOT_SET}"
```

If `NOT_SET` → print Setup Guide above and stop.

### 1. Transcribe

Run the transcription script:

```bash
VOLCENGINE_ASR_API_KEY="$VOLCENGINE_ASR_API_KEY" python3 ~/selfOS/scripts/transcribe.py "<file_path>" -o /tmp/transcript-output.md
```

Constraints:
- File must be < 100MB (极速版 limit)
- Audio must be < 2 hours
- Supported formats: mp3, wav, m4a, aac, ogg, opus, pcm, amr, spx

If file > 100MB, inform user and suggest trimming or using the batch API.

### 2. Review Output

Read the transcript from `/tmp/transcript-output.md`. Present a summary to the user:
- Duration
- Number of speakers detected
- First few lines preview
- Ask: "要归档到 wiki 吗？"

### 3. Archive Raw Transcript

Save raw transcript to `raw/` with descriptive filename:

```
raw/meeting-YYYY-MM-DD-<slug>-transcript.md
```

### 4. Wiki Ingest (if user confirms)

Create a wiki source page `wiki/sources/cc-YYYY-MM-DD-<slug>.md` with:

```yaml
---
title: "<meeting/recording description>"
type: source
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
tags: [meeting, transcript, ...]
summary: "<one-line summary of content>"
source_type: "audio-transcript"
---
```

Body should contain:
- Context section (who, when, why)
- Key points / decisions extracted from transcript
- Action items if any
- Full transcript in a collapsible section or appendix reference

### 5. Update Index + Log

- Add entry to `wiki/index.md`
- Append to `wiki/log.md`
- Cross-link to relevant entity/concept pages

### 6. Confirm

```
### 🎙️ 转写完成

- 时长: XX分XX秒
- 说话人: N 位
- 原文: raw/<filename>
- Wiki: wiki/sources/<filename>

已归档到 wiki。
```

## Speaker Mapping

If user identifies speakers (e.g., "Speaker 1 是浩，Speaker 2 是我"), replace speaker labels in the wiki source page with actual names.

## Edge Cases

- **File not found**: Check common locations (Downloads, Desktop, WeChat temp)
- **API key missing**: Print setup instructions (console.volcengine.com/speech/app)
- **Transcription fails**: Show error, suggest checking file format/size
- **Multiple files**: Process sequentially, each gets its own source page
- **Non-Chinese audio**: Still works (supports 23 languages), but Chinese is primary

## Common Mistakes

- Forgetting to save raw transcript before wiki processing
- Not asking user to identify speakers before finalizing wiki page
- Creating wiki page without user confirmation
- Losing transcript if wiki ingest fails — always save raw first
