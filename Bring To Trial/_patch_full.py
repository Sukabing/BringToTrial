# -*- coding: utf-8 -*-
"""正式版专属设置：自动存档、标题背景、字号档位、选项悬浮词条 + 词条阐释层。

可重复运行：每处都要求唯一命中，已改过的会报「命中 0 次」并退出，不会重复叠加。
"""
import sys
from pathlib import Path

GAME = Path(r"E:\Projects\RenPy\Bring To Trial\game")

OPTIONS = [
    ('define config.has_voice = True',
     'define config.has_voice = True\n'
     '\n'
     '## 每到选择支自动存一档（Ren\'Py 默认即开启，这里写明意图；读档界面有「自动存档」页）\n'
     'define config.has_autosave = True\n'
     'define config.autosave_on_choice = True'),
]

GUI = [
    ('define gui.main_menu_background = "gui/main_menu.png"',
     '## 标题界面背景：美术资源「1.初遇圣人 第11页」\ndefine gui.main_menu_background = "art/art03_meet_sages.jpg"'),
]

SCREENS = [
    ('        text what id "what"',
     '        text what id "what" size (say_text_size())'),
    ('                text who id "who"',
     '                text who id "who" size (say_name_size())'),

    ('''screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action''',
     '''screen choice(items):
    style_prefix "choice"

    on "show" action SetVariable("menu_tip", "")

    vbox:
        for i in items:
            textbutton i.caption:
                action i.action
                hovered SetVariable("menu_tip", menu_hint(i.caption))
                unhovered SetVariable("menu_tip", "")
                text_size (say_choice_size())

    ## 选择支下方常驻一条说明：平时是提示语，鼠标落到某个选项上就换成该词条的阐释
    frame:
        xalign 0.5
        ypos 520
        xsize 1400
        padding (26, 18)
        background "#0b1016dd"

        text (menu_tip or t("—— 将鼠标移到选项上，查看该词条的阐释 ——", "— Hover a choice to read its glossary note —")):
            style "choice_tip_body"
            xsize 1348'''),

    ('''style choice_button_text is default:
    properties gui.text_properties("choice_button")''',
     '''style choice_button_text is default:
    properties gui.text_properties("choice_button")

style choice_tip_body is default:
    size 22
    line_spacing 8
    color gui.idle_small_color'''),

    ('                ## 可在此处添加 radio_pref 或 check_pref 类型的额外 vbox，以添加',
     '''                vbox:
                    style_prefix "radio"
                    label _("字号")
                    textbutton _("小") action [SetField(persistent, "text_scale", 0), Function(renpy.restart_interaction)] selected (persistent.text_scale == 0)
                    textbutton _("标准") action [SetField(persistent, "text_scale", 1), Function(renpy.restart_interaction)] selected (persistent.text_scale == 1)
                    textbutton _("大") action [SetField(persistent, "text_scale", 2), Function(renpy.restart_interaction)] selected (persistent.text_scale == 2)

                ## 可在此处添加 radio_pref 或 check_pref 类型的额外 vbox，以添加'''),
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
patch("gui.rpy", GUI)
patch("screens.rpy", SCREENS)
