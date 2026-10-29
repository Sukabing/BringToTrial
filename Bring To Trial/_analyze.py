# -*- coding: utf-8 -*-
"""分析完整版 script.rpy：菜单选项、角色台词、配音 id。"""
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

SRC = Path(r"E:\Projects\RenPy\Bring To Trial\game\script.rpy")
lines = SRC.read_text(encoding="utf-8").split("\n")

SPEAKERS = {"narrator": "旁白", "s": "少年", "lu": "鲁鄹邑人", "ga": "加利利拿撒勒人",
            "conf": "孔门儒生", "monk": "苦行修士司祭", "unknown": "未知声音",
            "other": "其他"}

# ---- 菜单选项 ----
menus = []
for i, ln in enumerate(lines):
    if ln.strip() == "menu:" and i > 0:
        opts = []
        for j in range(i, min(i + 12, len(lines))):
            m = re.match(r'\s+"\[opt_([abc])\]":', lines[j])
            if m:
                opts.append(j)
        if opts:
            first = opts[0]
            hint = lines[first - 1].strip() if first > 0 else ""
            menus.append((i + 1, opts))

print(f"=== 选择菜单 {len(menus)} 个 ===")
for line_no, opt_lines in menus:
    print(f"  line {line_no}" + (f"  (前一行: {lines[opt_lines[0]-1].strip()[:40]})" if opt_lines else ""))

# ---- 每个 opt 的原文（$ opt_x = t(...) 里的中文） ----
print("\n=== 选项中文原文 ===")
for i, ln in enumerate(lines):
    m = re.match(r'\s+\$ opt_([abc]) = t\("([^"]+)"', ln)
    if m:
        print(f"  {i+1}: opt_{m.group(1)} = {m.group(2)}")

# ---- 角色与配音 ----
cur_voice = None
rows = []
for i, ln in enumerate(lines):
    mv = re.match(r'\s+voice "([^"]+)"', ln)
    if mv:
        cur_voice = mv.group(1)
        continue
    mline = re.match(r'\s+\$ line = t\("((?:[^"\\]|\\.)*)", "((?:[^"\\]|\\.)*)"\)', ln)
    if mline and cur_voice:
        zh, en = mline.group(1), mline.group(2)
        speaker = None
        for j in range(i + 1, min(i + 3, len(lines))):
            ms = re.match(r'\s+(\w+) "\[line\]"', lines[j])
            if ms:
                speaker = ms.group(1)
                break
        rows.append((cur_voice, speaker, zh, en))
        cur_voice = None
    elif re.match(r'\s+\w+ "\[line\]"', ln):
        cur_voice = None

print(f"\n=== 配音行 {len(rows)} 条 ===")
by_prefix = Counter(r[0].rsplit("_", 1)[0] for r in rows)
for k, v in by_prefix.most_common():
    print(f"  {k:<16} {v:>3}")
by_speaker = Counter(r[1] for r in rows)
print("\n=== 按角色 ===")
for k, v in by_speaker.most_common():
    print(f"  {str(k):<10} {v:>3}  ({SPEAKERS.get(k, '?')})")

print("\n=== 样例（每种前缀第一条） ===")
seen = set()
for vid, spk, zh, en in rows:
    p = vid.rsplit("_", 1)[0]
    if p in seen:
        continue
    seen.add(p)
    print(f"  {vid}  [{spk}]  {zh[:36]}")
