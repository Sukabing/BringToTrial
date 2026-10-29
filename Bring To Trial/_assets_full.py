# -*- coding: utf-8 -*-
"""把美术资源全部（33 张）转成 1920x1080 jpg，放进正式版 game/art。"""
import subprocess
import sys
from pathlib import Path

SRC = Path(r"E:\Projects\RenPy\Bring To Trial\美术资源（豆包")
DST = Path(r"E:\Projects\RenPy\Bring To Trial\game\art")
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
    ("审判2 60页-65 少年依旧阴郁.jpeg", "art18_gloomy"),
    ("66页 孔子 选择3.jpeg", "art19_choice3"),
    ("67页 西方圣人 选择4.jpeg", "art20_choice4"),
    ("68页-75  少年困顿开口.jpeg", "art21_struggle"),
    ("76页-审判2结束 少年看他们.jpeg", "art22_look_at_them"),
    ("77页-92 少年绝望 审判3开始.jpeg", "art23_despair"),
    ("93 孔子 选择5.jpeg", "art24_choice5"),
    ("94-审判3结束  西方圣人 选择6.jpeg", "art25_choice6"),
    ("95-97 少年抬头.jpeg", "art26_look_up"),
    ("98 走出少年2.jpeg", "art27_walk_out"),
    ("99- 109 少年面对面.jpeg", "art28_face_to_face"),
    ("110 儒生苦行说话 选择7.jpeg", "art29_choice7"),
    ("111-114 少年问 选择8和9 结束审判全过程.jpeg", "art30_ask"),
    ("115-117 走出小屋 结尾段.jpeg", "art31_leave"),
    ("118-122 少年回头看圣人.jpeg", "art32_look_back"),
    ("结尾 少年跑向旷野.jpeg", "art33_field"),
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
    ok += 1

total = sum(p.stat().st_size for p in DST.glob("*.jpg")) / 1024 / 1024
print(f"{ok}/{len(PAIRS)} 张已转换，共 {total:.1f} MB -> {DST}")
sys.exit(0 if ok == len(PAIRS) else 1)
