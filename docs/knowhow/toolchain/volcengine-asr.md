# 火山引擎 ASR（录音转写）

> Volcengine 大模型录音文件识别极速版 — 单次请求同步返回，支持说话人分离

## Problem
需要把 meeting 录音（mp3/m4a）转成带时间戳+说话人标记的文字，用于 wiki 归档。

## Cause
本地 Whisper 太慢且无 speaker diarization；火山引擎 ASR 有 20h 免费额度，极速版同步返回。

## Solution

### 认证
- API Key 模式（新版控制台）
- 环境变量: `VOLCENGINE_ASR_API_KEY`
- 控制台: https://console.volcengine.com/speech/app

### 产品选择
| 产品 | 适用 | 价格 |
|------|------|------|
| 极速版 | < 2h / 100MB，同步返回 | 4.5 元/h（免费 20h） |
| 标准版 | 2-5h，异步轮询 | 2.3 元/h |
| 闲时版 | 大批量不急 | 1.2 元/h |
| 豆包 2.0 | 性价比最高 | 0.8 元/h |

### 关键参数
```json
{
  "enable_itn": true,
  "enable_punc": true,
  "show_utterances": true,
  "enable_speaker_info": true
}
```

### 支持格式
mp3, wav, m4a, aac, ogg, opus, pcm, amr, spx（采样率无限制）

## Commands
```bash
# 设置 API Key
export VOLCENGINE_ASR_API_KEY="your-key"

# 转写本地文件
python3 ~/selfOS/scripts/transcribe.py recording.mp3

# 输出到文件
python3 ~/selfOS/scripts/transcribe.py meeting.m4a -o /tmp/transcript.md

# 输出原始 JSON
python3 ~/selfOS/scripts/transcribe.py recording.wav --json
```

## Notes
- Date: 2026-05-18
- Endpoint: `https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash`
- Resource ID: `volc.bigasr.auc_turbo`
- Skill: `/transcribe`（selfOS skill，自动检测 key + 引导设置）
- Script: `scripts/transcribe.py`
