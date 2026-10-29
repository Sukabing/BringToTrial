# -*- coding: utf-8 -*-
"""把美术资源里演示版用到的那批图，等比缩到 1920x1080 的 jpg。"""
import subprocess
import sys
from pathlib import Path

SRC = Path(r"E:\Projects\RenPy\Bring To Trial\美术资源（豆包")
DST = Path(r"E:\Projects\RenPy\BringToTrial-Demo\game\art")
FFMPEG = Path(r"C:\Users\sukab\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe")

PAIRS = [
    ("1.少年进门 第1页-2页.png", "art01_entry"),
    ("1.缓步前行 第3页-10页.jpeg", "art02_walk"),
    ("1.初遇圣人 第11页.png", "art03_meet_sages"),
    ("1.看见孔子 第12页.png", "art04_confucius"),
    ("第13页 看见西方面孔.jpeg", "art05_west_sage"),
    ("14页-17，看见两个圣人很惊讶.jpeg", "art06_two_sages"),
    ("18-21页，甜腻微笑.jpeg", "art07_sweet_smile"),
    ("22页 孔门儒生出现.jpeg", "art08_scholar"),
    ("23页 苦行修士出现.jpeg", "art09_monk"),
    ("26页 惊愕到微笑.jpeg", "art10_shock_to_smile"),
    ("31页 转为内心怒火.jpeg", "art11_inner_anger"),
    ("审判1  34页 语气不屑.jpeg", "art12_disdain"),
    ("39页 孔子  选择一.jpeg", "art13_choice_scholar"),
    ("40页 西方圣人 选择二.jpeg", "art14_choice_west"),
    ("41-43页 放肆笑.jpeg", "art15_wild_laugh"),
    ("44页-58 三人对峙.jpeg", "art16_standoff"),
    ("59页- 审判1结束   少年领悟.jpeg", "art17_realize"),
]

DST.mkdir(parents=True, exist_ok=True)
ok = 0
for name, out in PAIRS:
    src = SRC / name
    if not src.is_file():
        print(f"MISSING: {name}")
        continue
    target = DST / (out + ".jpg")
    cmd = [str(FFMPEG), "-y", "-hide_banner", "-loglevel", "error",
           "-i", str(src), "-vf", "scale=1920:1080:flags=lanczos",
           "-q:v", "3", "-pix_fmt", "yuvj420p", str(target)]
    if subprocess.run(cmd).returncode != 0:
        print(f"FAIL: {name}")
        continue
    print(f"OK {out:<22} {target.stat().st_size // 1024:>5} KB")
    ok += 1

print(f"\n{ok}/{len(PAIRS)} converted")
sys.exit(0 if ok == len(PAIRS) else 1)
