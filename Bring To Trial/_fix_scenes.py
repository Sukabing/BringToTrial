# -*- coding: utf-8 -*-
"""修分镜位置：有几处 scene 被插在 label 前一行，而上一条语句是 jump，导致永远执行不到。

规则：`    scene artXX with fade` 紧挨着 `label ...:` 时，把它移到 label 之后。
另把 art23_despair 挪到「第三审：脱离根基」标题之后，避免和 art22 贴脸。
"""
import re
import sys
from pathlib import Path

SCRIPT = Path(r"E:\Projects\RenPy\Bring To Trial\game\script.rpy")

lines = SCRIPT.read_text(encoding="utf-8").split("\n")
moved = []

i = 0
while i < len(lines) - 1:
    if lines[i].startswith("    scene art") and lines[i + 1].startswith("label "):
        scene = lines.pop(i)
        # pop 之后 label 上移一位
        lines.insert(i + 1, scene)
        moved.append(f"{scene.strip()} → 移到 {lines[i].strip()} 之后")
        i += 2
        continue
    i += 1

# art23_despair 挪到 第三审 标题之后
try:
    idx = lines.index("    scene art23_despair with fade")
except ValueError:
    idx = -1
if idx >= 0:
    title = next(k for k, l in enumerate(lines) if "—— 第三审：脱离根基 ——" in l)
    if idx < title:
        scene = lines.pop(idx)
        lines.insert(title + 2, scene)  # 标题行 + narrator 行之后
        moved.append("art23_despair → 挪到「第三审」标题之后")

SCRIPT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(moved) if moved else "没有需要移动的 scene")
print(f"当前行数: {len(lines)}")
