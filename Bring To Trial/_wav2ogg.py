# -*- coding: utf-8 -*-
"""把 TTS 生成的 wav 统一响度并转成 ogg，放进正式版 game/。"""
import subprocess
import sys
from pathlib import Path

WORK = Path(r"E:\Projects\Live\tts_out\wav")
GAME = Path(r"E:\Projects\RenPy\Bring To Trial\game")
FFMPEG = Path(r"C:\Users\sukab\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe")

wavs = sorted(WORK.glob("*.wav"))
if not wavs:
    sys.exit("没有 wav 可转")

done = skipped = failed = 0
total_bytes = 0
for wav in wavs:
    out = GAME / (wav.stem + ".ogg")
    if out.exists() and out.stat().st_mtime >= wav.stat().st_mtime:
        skipped += 1
        continue
    r = subprocess.run(
        [str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error", "-i", str(wav),
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1", "-ar", "44100",
         "-c:a", "libvorbis", "-q:a", "4", str(out)],
        capture_output=True, text=True)
    if r.returncode != 0:
        failed += 1
        print(f"FAIL {wav.name}: {r.stderr.strip()[:120]}")
        continue
    done += 1
    total_bytes += out.stat().st_size

print(f"转换 {done}，跳过 {skipped}，失败 {failed}，新增 {total_bytes / 1024 / 1024:.1f} MB")
print(f"game/ 里现有 ogg: {len(list(GAME.glob('*.ogg')))} 个")
