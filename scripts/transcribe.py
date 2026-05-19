#!/usr/bin/env python3
"""
火山引擎 ASR 录音转写脚本
用法:
    python3 scripts/transcribe.py <audio_file_or_url> [--output wiki/sources/xxx.md]
    python3 scripts/transcribe.py recording.m4a
    python3 scripts/transcribe.py https://oss.example.com/meeting.mp3 -o output.md

需要环境变量:
    VOLCENGINE_ASR_API_KEY — 从 https://console.volcengine.com/speech/app 创建

支持格式: mp3, wav, m4a, aac, ogg, opus, pcm, amr, spx
"""

import argparse
import base64
import json
import os
import sys
import uuid
from pathlib import Path

import requests


ENDPOINT = "https://openspeech.bytedance.com/api/v3/auc/bigmodel/recognize/flash"
RESOURCE_ID = "volc.bigasr.auc_turbo"


def get_api_key() -> str:
    key = os.environ.get("VOLCENGINE_ASR_API_KEY")
    if not key:
        print("Error: VOLCENGINE_ASR_API_KEY 环境变量未设置", file=sys.stderr)
        print("请到 https://console.volcengine.com/speech/app 创建 API Key", file=sys.stderr)
        sys.exit(1)
    return key


def file_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def transcribe(file_path: str = None, file_url: str = None) -> dict:
    """调用极速版 API 转写音频"""
    api_key = get_api_key()

    headers = {
        "X-Api-Key": api_key,
        "X-Api-Resource-Id": RESOURCE_ID,
        "X-Api-Request-Id": str(uuid.uuid4()),
        "X-Api-Sequence": "-1",
        "Content-Type": "application/json",
    }

    if file_url:
        audio_data = {"url": file_url}
    elif file_path:
        size_mb = Path(file_path).stat().st_size / (1024 * 1024)
        if size_mb > 100:
            print(f"Error: 文件 {size_mb:.1f}MB 超过极速版 100MB 限制", file=sys.stderr)
            sys.exit(1)
        print(f"正在编码文件 ({size_mb:.1f}MB)...", file=sys.stderr)
        audio_data = {"data": file_to_base64(file_path)}
    else:
        raise ValueError("必须提供 file_path 或 file_url")

    payload = {
        "user": {"uid": "selfos-transcriber"},
        "audio": audio_data,
        "request": {
            "model_name": "bigmodel",
            "enable_itn": True,
            "enable_punc": True,
            "enable_ddc": False,
            "show_utterances": True,
            "enable_speaker_info": True,
        },
    }

    print("正在转写...", file=sys.stderr)
    response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=300)
    response.raise_for_status()

    result = response.json()
    if result.get("code") != 0 and result.get("code") is not None:
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    return result


def format_transcript(result: dict) -> str:
    """格式化转写结果为 markdown"""
    lines = []

    resp = result.get("result", result.get("resp", {}))
    full_text = resp.get("text", "")
    utterances = resp.get("utterances", [])

    if utterances:
        for utt in utterances:
            start_s = utt.get("start_time", 0) / 1000
            end_s = utt.get("end_time", 0) / 1000
            text = utt.get("text", "")
            speaker = utt.get("additions", {}).get("speaker", "")

            if speaker:
                lines.append(f"[{start_s:.1f}s] **Speaker {speaker}**: {text}")
            else:
                lines.append(f"[{start_s:.1f}s] {text}")
    elif full_text:
        lines.append(full_text)

    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="火山引擎 ASR 录音转写")
    parser.add_argument("input", help="音频文件路径或 URL")
    parser.add_argument("-o", "--output", help="输出文件路径 (默认 stdout)")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    args = parser.parse_args()

    is_url = args.input.startswith("http://") or args.input.startswith("https://")

    if is_url:
        result = transcribe(file_url=args.input)
    else:
        if not Path(args.input).exists():
            print(f"Error: 文件不存在: {args.input}", file=sys.stderr)
            sys.exit(1)
        result = transcribe(file_path=args.input)

    if args.json:
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = format_transcript(result)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)

    print("完成!", file=sys.stderr)


if __name__ == "__main__":
    main()
