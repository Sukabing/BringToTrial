# -*- coding: utf-8 -*-
"""把演示版做过的改动落到正式版 game/script.rpy：开场梗概、33 张分镜、选择支简略词条、字号函数。

可重复运行：每一步都带标记，已改过的跳过。首次运行会把原脚本备份成 script.rpy.orig。
"""
import re
import shutil
import sys
from pathlib import Path

GAME = Path(r"E:\Projects\RenPy\Bring To Trial\game")
SRC = GAME / "script.rpy"

ART = ["art01_entry", "art02_walk", "art03_meet_sages", "art04_confucius", "art05_west_sage",
       "art06_two_sages", "art07_sweet_smile", "art08_scholar", "art09_monk", "art10_shock_to_smile",
       "art11_inner_anger", "art12_disdain", "art13_choice_scholar", "art14_choice_west",
       "art15_wild_laugh", "art16_standoff", "art17_realize", "art18_gloomy", "art19_choice3",
       "art20_choice4", "art21_struggle", "art22_look_at_them", "art23_despair", "art24_choice5",
       "art25_choice6", "art26_look_up", "art27_walk_out", "art28_face_to_face", "art29_choice7",
       "art30_ask", "art31_leave", "art32_look_back", "art33_field", "art34_run_dark"]

# (锚点子串, 第几次出现, 图片名, before|after)
ANCHORS = [
    ("怀着难以抑制的好奇与恐惧，少年蹀躞徐行", 1, "art02_walk", "before"),
    ("终于，在火光的尽头，他看见了那两个他既熟稔而又陌生的人", 1, "art03_meet_sages", "before"),
    ("其中一人身形高大，头顶微凹", 1, "art04_confucius", "before"),
    ("另一人的样貌普通平凡", 1, "art05_west_sage", "before"),
    ("少年大骇，因为他一眼便认出了前者", 1, "art06_two_sages", "before"),
    ("「他们那些胶柱鼓瑟的旧思想", 1, "art07_sweet_smile", "before"),
    ("为了审判你！", 1, "art08_scholar", "before"),
    ("在两位圣人身后的两侧分别走出了一位孔门儒生与一位苦行修士司祭", 1, "art09_monk", "before"),
    ("少年错愕不已，但很快又恢复了镇定", 1, "art10_shock_to_smile", "before"),
    ("少年感到诧异，心里陡地生起一股无名火", 1, "art11_inner_anger", "before"),
    ("你们既要审判我，那便来吧！无需装神弄鬼", 1, "art12_disdain", "before"),
    ("# 鲁鄹邑人三选一", 1, "art13_choice_scholar", "before"),
    ("# 加利利拿撒勒人三选一", 1, "art14_choice_west", "before"),
    ("少年放肆地笑道，眼里闪烁着轻蔑与挑衅", 1, "art15_wild_laugh", "before"),
    ("空口无凭，那你们在这方面的修为又如何", 1, "art16_standoff", "before"),
    ("少年沉思了一阵，他觉得自己理解得过于肤浅", 1, "art17_realize", "before"),

    ("# ========== 第二审：虚无 ==========", 1, "art18_gloomy", "before"),
    ("# 鲁鄹邑人三选一", 2, "art19_choice3", "before"),
    ("label ga_emptiness_choice:", 1, "art20_choice4", "after"),
    ("label youth_emptiness_q:", 1, "art21_struggle", "after"),
    ("label emptiness_end:", 1, "art22_look_at_them", "after"),
    ('voice "vo_narr_036.ogg"', 1, "art23_despair", "before"),
    ("# 鲁鄹邑人三选一", 3, "art24_choice5", "before"),
    ("label ga_root_choice:", 1, "art25_choice6", "after"),
    ("label verdict_start:", 1, "art26_look_up", "after"),
    ("在一阵沉默之后，从两位圣徒的身后传出的一阵熟悉而又陌生的脚步声", 1, "art27_walk_out", "before"),
    ("你也是来审判我的吗？", 1, "art28_face_to_face", "before"),
    ("# 孔门儒生三选一", 2, "art29_choice7", "before"),
    ("label youth_amend:", 1, "art30_ask", "after"),
    ("label ending:", 1, "art31_leave", "after"),
    ("他回头望向那座还不曾离远的小屋", 1, "art32_look_back", "before"),
    ("然后默默地转身，向远处的旷野奔去", 1, "art33_field", "before"),
]

HELPERS = '''default menu_tip = ""
default persistent.text_scale = 1

init python:
    ## 菜单上的简略词条：把「聆听「德本财末」」这类原文本压成「德本财末」
    def tag(full):
        for prefix in ("聆听", "Hear:"):
            if full.startswith(prefix):
                return full[len(prefix):].strip()
        return full

    ## 字号档位：小 / 标准 / 大。运行时改 style 不生效，所以大小由 say 屏和选项按钮直接读下面这几个函数
    TEXT_SCALES = (0.85, 1.0, 1.2)

    def text_scale():
        try:
            return TEXT_SCALES[persistent.text_scale]
        except (IndexError, TypeError):
            return 1.0

    def say_text_size():
        return int(gui.text_size * text_scale())

    def say_name_size():
        return int(gui.name_text_size * text_scale())

    def say_choice_size():
        return int(gui.choice_button_text_size * text_scale())

    ## 选项下方的说明：有词条阐释就显示阐释，文档里没有的词条给一句占位
    def menu_hint(caption):
        caption = renpy.substitute(caption)
        tip = globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")
        return tip or t("「%s」暂无阐释", "\\"%s\\": no note yet") % caption.strip("「」")

'''

SYNOPSIS_ZH = ("【故事梗概】\\n\\n"
               "铁门之内，那两位被亿万人顶礼膜拜的圣人——鲁鄹邑人与加利利拿撒勒人——正在等他。\\n"
               "少年不信他们那套旧道理，只想用自己时代的智慧把他们驳倒。\\n"
               "于是他等来的不是辩论，而是一场审判：先问物质，再问虚无，最后问那道谁也绕不开的根基。\\n"
               "而自始至终，被审判的都是他自己。")

SYNOPSIS_EN = ("【Synopsis】\\n\\n"
               "Behind the iron gate, two men revered by countless millions — the Man of Zou and the Man of Nazareth — are waiting for him.\\n"
               "The youth does not believe a word of their old teaching, and means to refute them with the wisdom of his own age.\\n"
               "So what awaits him is not a debate but a trial: first materialism, then emptiness, and at last the root no one can walk around.\\n"
               "And all along, he is the one on trial.")

SYNOPSIS = (
    '    # ========== 开场：黑屏故事梗概 ==========\n'
    '    scene black\n'
    '    $ line = t("%s", "%s")\n'
    '    centered "[line]"\n'
    '\n'
    '    scene art01_entry with fade'
) % (SYNOPSIS_ZH, SYNOPSIS_EN)


def main():
    if not SRC.is_file():
        sys.exit(f"找不到 {SRC}")
    backup = SRC.with_suffix(".rpy.orig")
    if not backup.exists():
        shutil.copy2(SRC, backup)
        print(f"已备份原脚本 -> {backup.name}")

    text = SRC.read_text(encoding="utf-8")
    report = []

    # ---- 1. 开场梗概 + 第一页 ----
    if "【故事梗概】" in text:
        report.append("梗概: 已有，跳过")
    elif "    scene bg room with fade" in text:
        text = text.replace("    scene bg room with fade", SYNOPSIS, 1)
        report.append("梗概: 已插入")
    else:
        sys.exit("找不到 scene bg room，放弃")

    # ---- 2. 分镜插入 ----
    lines = text.split("\n")
    added = skipped = 0
    for needle, occ, img, where in ANCHORS:
        if f"scene {img} with fade" in text:
            skipped += 1
            continue
        hits = [i for i, ln in enumerate(lines) if needle in ln]
        if len(hits) < occ:
            sys.exit(f"锚点出现 {len(hits)} 次，需要第 {occ} 次：{needle}")
        pos = hits[occ - 1] + (1 if where == "after" else 0)
        lines.insert(pos, f"    scene {img} with fade")
        added += 1
    text = "\n".join(lines)
    report.append(f"分镜: 新增 {added}，跳过 {skipped}")

    # ---- 3. 选择菜单：简略词条 ----
    lines = text.split("\n")
    if any("$ tag_a, tag_b, tag_c = tag(" in ln for ln in lines):
        report.append("词条菜单: 已有，跳过")
    else:
        out, i, menus = [], 0, 0
        while i < len(lines):
            ln = lines[i]
            if ln == "    menu:" and any("    $ opt_a = " in x for x in lines[max(0, i - 12):i]):
                out.append("    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)")
                out.append(ln)
                i += 1
                while i < len(lines) and (lines[i].startswith("        ") or lines[i] == ""):
                    m = re.match(r'^( {8})"\[opt_([abc])\]":$', lines[i])
                    out.append(f'{m.group(1)}"[tag_{m.group(2)}]":' if m else lines[i])
                    i += 1
                menus += 1
                continue
            out.append(ln)
            i += 1
        text = "\n".join(out)
        report.append(f"词条菜单: 改写 {menus} 个")

    # ---- 4. 辅助函数 ----
    if "def say_text_size()" in text:
        report.append("字号函数: 已有，跳过")
    else:
        if text.count("# ---------- 角色定义 ----------") != 1:
            sys.exit("找不到角色定义段，放弃")
        text = text.replace("# ---------- 角色定义 ----------", HELPERS + "# ---------- 角色定义 ----------", 1)
        report.append("字号函数: 已插入")

    # ---- 5. 图片定义 ----
    if "art33_field = " in text:
        report.append("图片定义: 已有，跳过")
    else:
        defs = "\n".join(f'image {a} = "art/{a}.jpg"' for a in ART)
        block = "# ---------- 美术资源（豆包生成，第1-122页） ----------\n" + defs + "\n\nlabel start:"
        if text.count("label start:") != 1:
            sys.exit("label start 不唯一，放弃")
        text = text.replace("label start:", block, 1)
        report.append(f"图片定义: 插入 {len(ART)} 条")

    # ---- 6. 坏结局收尾图（奔向黑暗） ----
    BAD_OLD = '    scene art33_field with fade\n    $ line = t("少年冷笑道'
    BAD_NEW = '    scene art34_run_dark with fade\n    $ line = t("少年冷笑道'
    if "art34_run_dark = " not in text:
        text = text.replace('image art33_field = "art/art33_field.jpg"',
                            'image art33_field = "art/art33_field.jpg"\n'
                            'image art34_run_dark = "art/art34_run_dark.jpg"', 1)
        report.append("坏结局配图: 已加定义")
    if BAD_OLD in text:
        text = text.replace(BAD_OLD, BAD_NEW, 1)
        report.append("坏结局配图: 已切到 art34_run_dark")

    SRC.write_text(text, encoding="utf-8")
    print("\n".join(report))
    print(f"结果: {len(text.splitlines())} 行 -> {SRC}")


main()
