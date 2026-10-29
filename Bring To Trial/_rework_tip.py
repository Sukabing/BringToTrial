# -*- coding: utf-8 -*-
"""把悬浮提示改成「选中选择支就显示该词条的阐释」：改 screens.rpy 的 choice 屏与 script.rpy 的 menu_hint。

两个工程都改（正式版 + 演示版），每处要求唯一命中。
"""
import sys
from pathlib import Path

PROJECTS = [Path(r"E:\Projects\RenPy\Bring To Trial"),
            Path(r"E:\Projects\RenPy\BringToTrial-Demo")]

OLD_CHOICE = '''screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption:
                action i.action
                hovered SetVariable("menu_tip", menu_hint(i.caption))
                unhovered SetVariable("menu_tip", "")
                text_size (say_choice_size())

    ## 右上角：打开「词条阐释」全文
    textbutton _("词条"):
        action Show("citao")
        xalign 0.985
        yalign 0.045
        background None
        padding (12, 6)
        text_size 24
        text_idle_color gui.idle_small_color
        text_hover_color gui.hover_color

    ## 鼠标悬浮在某个选项上时，在选项下方显示它的原文本与词条要点
    text "[menu_tip]":
        style "choice_tip"
        xalign 0.5
        xmaximum 1500
        ypos 545'''

NEW_CHOICE = '''screen choice(items):
    style_prefix "choice"

    on "show" action SetVariable("menu_tip", "")

    vbox:
        for i in items:
            textbutton i.caption:
                action i.action
                hovered SetVariable("menu_tip", menu_hint(i.caption))
                unhovered SetVariable("menu_tip", "")
                text_size (say_choice_size())

    ## 鼠标落在某个选择支上时，在下方摊开该词条的阐释，帮玩家看懂这一支讲的是什么
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

OLD_STYLES = '''style choice_tip is default:
    size 24
    line_spacing 6
    color gui.idle_small_color

## 词条阐释全屏层
screen citao():
    modal True
    zorder 150

    add Solid("#05080cf2")

    vbox:
        xalign 0.5
        yalign 0.5
        xsize 1520
        ysize 920
        spacing 14

        hbox:
            xfill True
            text _("词条阐释"):
                style "citao_title"
            textbutton _("关闭"):
                action Hide("citao")
                xalign 1.0
                text_size 24

        viewport:
            scrollbars "vertical"
            mousewheel True
            ysize 820

            vbox:
                spacing 28
                for name in sorted(CITAO):
                    text "「[name]」":
                        style "citao_title"
                    text CITAO[name]:
                        style "citao_body"

    key "game_menu" action Hide("citao")

style citao_title is default:
    size 30
    color gui.accent_color

style citao_body is default:
    size 22
    line_spacing 8
    color gui.text_color'''

NEW_STYLES = '''style choice_tip_body is default:
    size 22
    line_spacing 8
    color gui.idle_small_color'''

OLD_HINT = '''    ## 悬浮提示：原文本 + 该词条在「词条阐释」里的出处与核心思想（文档里没有的词条只给原文本）
    def menu_hint(caption):
        full = menu_tips.get(caption, caption)
        tip = globals().get("CITAO_TIP", {}).get(caption.strip("「」"))
        return full + ("\\n" + tip if tip else "")'''

NEW_HINT = '''    ## 悬浮提示：该选择支词条在「词条阐释」里的解释（文档里没有的词条就不显示）
    def menu_hint(caption):
        return globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")'''


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        sys.exit(f"{path.name}: 命中 {n} 次，需唯一（1）：{old.splitlines()[0][:50]}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


for proj in PROJECTS:
    replace_once(proj / "game" / "screens.rpy", OLD_CHOICE, NEW_CHOICE)
    replace_once(proj / "game" / "screens.rpy", OLD_STYLES, NEW_STYLES)
    replace_once(proj / "game" / "script.rpy", OLD_HINT, NEW_HINT)
    print(f"{proj.name}: 悬浮阐释已改为选项内直接展开")
