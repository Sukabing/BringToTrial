# -*- coding: utf-8 -*-
"""选项下方改成常驻说明条：平时显示提示语，鼠标落到某个选项就换该词条的阐释。

改两个工程（正式版 + 演示版）的 screens.rpy 与 script.rpy。
"""
import sys
from pathlib import Path

PROJECTS = [Path(r"E:\Projects\RenPy\Bring To Trial"),
            Path(r"E:\Projects\RenPy\BringToTrial-Demo")]

OLD_PANEL = '''    ## 鼠标落在某个选择支上时，在下方摊开该词条的阐释，帮玩家看懂这一支讲的是什么
    if menu_tip:
        frame:
            xalign 0.5
            ypos 520
            xsize 1400
            padding (26, 18)
            background "#0b1016dd"

            text menu_tip:
                style "choice_tip_body"
                xsize 1348'''

NEW_PANEL = '''    ## 选择支下方常驻一条说明：平时是提示语，鼠标落到某个选项上就换成该词条的阐释
    frame:
        xalign 0.5
        ypos 520
        xsize 1400
        padding (26, 18)
        background "#0b1016dd"

        text (menu_tip or t("—— 将鼠标移到选项上，查看该词条的阐释 ——", "— Hover a choice to read its glossary note —")):
            style "choice_tip_body"
            xsize 1348'''

OLD_HINT = '''    ## 悬浮提示：该选择支词条在「词条阐释」里的解释（文档里没有的词条就不显示）
    def menu_hint(caption):
        return globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")'''

NEW_HINT = '''    ## 选项下方的说明：有词条阐释就显示阐释，文档里没有的词条给一句占位
    def menu_hint(caption):
        tip = globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")
        return tip or t("「%s」暂无阐释", "\\"%s\\": no note yet") % caption.strip("「」")'''


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        sys.exit(f"{path.name}: 命中 {n} 次，需唯一（1）：{old.splitlines()[0][:50]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


for proj in PROJECTS:
    replace_once(proj / "game" / "screens.rpy", OLD_PANEL, NEW_PANEL)
    replace_once(proj / "game" / "script.rpy", OLD_HINT, NEW_HINT)
    print(f"{proj.name}: 说明条改为常显")
