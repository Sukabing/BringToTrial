# -*- coding: utf-8 -*-
"""生成器里的 menu_hint 也要带插值（脚本源串里是 \\" 双反斜杠，单独处理）。"""
import sys
from pathlib import Path

TARGETS = [Path(r"E:\Projects\RenPy\Bring To Trial\_full.py"),
           Path(r"E:\Projects\RenPy\BringToTrial-Demo\_script.py")]

OLD = '''    def menu_hint(caption):
        tip = globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")'''

NEW = '''    def menu_hint(caption):
        caption = renpy.substitute(caption)
        tip = globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")'''

for path in TARGETS:
    text = path.read_text(encoding="utf-8")
    n = text.count(OLD)
    if n != 1:
        sys.exit(f"{path.name}: 命中 {n} 次，需唯一（1）")
    path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print(f"{path.name}: 生成器已同步插值")
