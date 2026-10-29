# -*- coding: utf-8 -*-
"""把 _full.py 里那 5 个分镜锚点改成修正后的位置。"""
from pathlib import Path

p = Path(r"E:\Projects\RenPy\Bring To Trial\_full.py")
s = p.read_text(encoding="utf-8")

PAIRS = [
    ('    ("label ga_emptiness_choice:", 1, "art20_choice4", "before"),',
     '    ("label ga_emptiness_choice:", 1, "art20_choice4", "after"),'),
    ('    ("label emptiness_end:", 1, "art22_look_at_them", "before"),',
     '    ("label emptiness_end:", 1, "art22_look_at_them", "after"),'),
    ('    ("label emptiness_end:", 1, "art23_despair", "after"),',
     "    ('voice \"vo_narr_036.ogg\"', 1, \"art23_despair\", \"before\"),"),
    ('    ("label ga_root_choice:", 1, "art25_choice6", "before"),',
     '    ("label ga_root_choice:", 1, "art25_choice6", "after"),'),
    ('    ("label youth_amend:", 1, "art30_ask", "before"),',
     '    ("label youth_amend:", 1, "art30_ask", "after"),'),
]

for old, new in PAIRS:
    if s.count(old) != 1:
        raise SystemExit(f"未命中或重复: {old}")
    s = s.replace(old, new, 1)

p.write_text(s, encoding="utf-8")
print("_full.py 锚点已修正 5 处")
