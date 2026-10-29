# -*- coding: utf-8 -*-
"""演示版专属设置：只改 options.rpy 里的身份信息。

screens.rpy / gui.rpy 直接沿用正式版（已含字号档位、选项悬浮阐释、标题背景），
所以这里不再重复打补丁。
"""
import sys
from pathlib import Path

GAME = Path(r"E:\Projects\RenPy\BringToTrial-Demo\game")

OPTIONS = [
    ('define config.name = _("Bring To Trial")',
     'define config.name = _("Bring To Trial — 演示版")'),
    ('define config.version = "1.0"',
     'define config.version = "1.0-demo"'),
    ('define gui.about = _p("""\n""")',
     'define gui.about = _p("""\n《三审少年》演示版。\n\n本版本收录至「第一审：物质」结束，美术由豆包生成。\n完整版包含第二审「虚无」与随后的裁决。\n""")'),
    ('define build.name = "BringToTrial"',
     'define build.name = "BringToTrialDemo"'),
    ('define config.has_voice = True',
     'define config.has_voice = False\n'
     '\n'
     '## 每到选择支自动存一档（Ren\'Py 默认即开启，这里写明意图；读档界面有「自动存档」页）\n'
     'define config.has_autosave = True\n'
     'define config.autosave_on_choice = True'),
    ('define config.save_directory = "BringToTrial-1791505582"',
     'define config.save_directory = "BringToTrialDemo-1791505582"'),
]


def patch(name: str, pairs) -> None:
    path = GAME / name
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{name}: 命中 {n} 次，需唯一（1）：{old.splitlines()[0][:60]}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print(f"{name}: {len(pairs)} 处已改")


patch("options.rpy", OPTIONS)
