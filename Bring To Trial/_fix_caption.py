# -*- coding: utf-8 -*-
"""修 bug：菜单 caption 是 "[tag_a]" 这种待插值字符串，menu_hint 直接拿它查表必然查不到。

查之前先 renpy.substitute 插值成「德本财末」。
"""
import sys
from pathlib import Path

TARGETS = [Path(r"E:\Projects\RenPy\Bring To Trial\game\script.rpy"),
           Path(r"E:\Projects\RenPy\BringToTrial-Demo\game\script.rpy"),
           Path(r"E:\Projects\RenPy\Bring To Trial\_full.py"),
           Path(r"E:\Projects\RenPy\BringToTrial-Demo\_script.py")]

OLD = '''    def menu_hint(caption):
        tip = globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")
        return tip or t("「%s」暂无阐释", "\\"%s\\": no note yet") % caption.strip("「」")'''

NEW = '''    def menu_hint(caption):
        caption = renpy.substitute(caption)
        tip = globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")
        return tip or t("「%s」暂无阐释", "\\"%s\\": no note yet") % caption.strip("「」")'''

for path in TARGETS:
    text = path.read_text(encoding="utf-8")
    n = text.count(OLD)
    if n != 1:
        sys.exit(f"{path.name}: 命中 {n} 次，需唯一（1）")
    path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print(f"{path.parent.name}/{path.name}: 已插值 caption")
