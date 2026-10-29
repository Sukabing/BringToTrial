# -*- coding: utf-8 -*-
"""用 IndexTTS-2.5 把正式版的 258 条台词全部配音（情感向量控制），输出 wav。

用法:
    python _tts_render.py --limit 2      # 先试两条
    python _tts_render.py                # 全量（可断点续跑，已存在的 wav 会跳过）
"""
import argparse
import csv
import subprocess
import sys
import time
from pathlib import Path

INDEX_TTS = Path(r"E:\index-tts")
sys.path.insert(0, str(INDEX_TTS))

PROJ = Path(r"E:\Projects\RenPy\Bring To Trial")
CSV = PROJ / "docs" / "voice_lines.csv"
REF_DIR = Path(r"E:\Projects\Live\临时")
WORK = Path(r"E:\Projects\Live\tts_out")
WAV_DIR = WORK / "wav"
REF_WAV = WORK / "refs"
FFMPEG = Path(r"C:\Users\sukab\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe")

# 声音映射：角色 -> (参考音频, 情感向量[喜,怒,哀,惧,厌恶,低落,惊喜,平静]，和 <= 0.8)
VOICES = {
    "narrator": ("无标题 旁白.mp3",       [0.00, 0.00, 0.10, 0.00, 0.00, 0.10, 0.00, 0.60]),
    "s":        ("无标题 少年.mp3",       [0.10, 0.35, 0.00, 0.00, 0.20, 0.00, 0.05, 0.10]),
    "lu":       ("无标题 鲁鄹邑人.mp3",   [0.05, 0.00, 0.05, 0.00, 0.00, 0.00, 0.00, 0.70]),
    "ga":       ("无标题 加利利.mp3",     [0.10, 0.00, 0.10, 0.00, 0.00, 0.00, 0.00, 0.60]),
    "conf":     ("无标题 孔门儒生.mp3",   [0.05, 0.05, 0.00, 0.00, 0.10, 0.00, 0.00, 0.60]),
    "monk":     ("无标题 苦行修士.mp3",   [0.00, 0.00, 0.15, 0.00, 0.00, 0.10, 0.00, 0.55]),
    "unknown":  ("无标题 未知声音.mp3",   [0.00, 0.00, 0.10, 0.10, 0.00, 0.10, 0.00, 0.50]),
    "other":    ("无标题 少年2.mp3",      [0.00, 0.00, 0.05, 0.00, 0.00, 0.15, 0.00, 0.60]),
}

# 少年的三段情绪弧线（按他自己的台词顺序均分）：傲慢 → 阴郁 → 啜泣绝望
S_ARCS = [
    [0.10, 0.35, 0.00, 0.00, 0.20, 0.00, 0.05, 0.10],
    [0.00, 0.10, 0.20, 0.05, 0.10, 0.25, 0.00, 0.10],
    [0.00, 0.05, 0.35, 0.10, 0.00, 0.25, 0.00, 0.05],
]


def prepare_refs() -> None:
    REF_WAV.mkdir(parents=True, exist_ok=True)
    for name, _ in VOICES.values():
        src = REF_DIR / name
        dst = REF_WAV / (src.stem + ".wav")
        if dst.exists() and dst.stat().st_size > 1000:
            continue
        subprocess.run([str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(src), "-ac", "1", "-ar", "24000", str(dst)], check=True)


def load_rows():
    with CSV.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    prepare_refs()
    WAV_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    s_total = sum(1 for r in rows if r["角色变量"] == "s")

    print(f"共 {len(rows)} 条台词，准备加载模型…", flush=True)
    from indextts.infer_v2_5 import IndexTTS2  # noqa: E402

    t0 = time.time()
    tts = IndexTTS2(cfg_path=str(INDEX_TTS / "checkpoints" / "config.yaml"),
                    model_dir=str(INDEX_TTS / "checkpoints"),
                    use_bf16=True, device="cuda:0",
                    use_cuda_kernel=False, use_deepspeed=False,
                    use_accel=False, use_torch_compile=False,
                    use_qwen_emo=False)
    print(f"模型加载完成 {time.time() - t0:.1f}s", flush=True)

    done = skipped = failed = 0
    s_seen = 0
    run_start = time.time()
    for i, row in enumerate(rows, 1):
        vid = row["voice_id"]
        out = WAV_DIR / (Path(vid).stem + ".wav")
        speaker = row["角色变量"]
        if speaker == "s":
            third = min(2, s_seen * 3 // max(s_total, 1))
            vec = S_ARCS[third]
            s_seen += 1
        else:
            vec = VOICES[speaker][1]

        if out.exists() and out.stat().st_size > 1000 and not args.force:
            skipped += 1
            continue

        ref = REF_WAV / (Path(VOICES[speaker][0]).stem + ".wav")
        t1 = time.time()
        try:
            tts.infer(spk_audio_prompt=str(ref), text=row["中文台词"],
                      output_path=str(out), lang="ZH",
                      emo_vector=vec, emo_alpha=1.0, verbose=False)
            done += 1
            print(f"[{i}/{len(rows)}] {vid} {speaker} {time.time() - t1:.1f}s", flush=True)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"[{i}/{len(rows)}] {vid} FAILED {type(exc).__name__}: {exc}", flush=True)

        if args.limit and done >= args.limit:
            print("达到 --limit，停止", flush=True)
            break

    print(f"完成: 新生成 {done}，跳过 {skipped}，失败 {failed}，"
          f"总耗时 {time.time() - run_start:.0f}s", flush=True)


if __name__ == "__main__":
    main()
