# -*- coding: utf-8 -*-
"""从正式版的原始脚本（script.rpy.orig）生成演示版：裁到第一审结束、去配音与 BGM、接美术、简略词条、开场梗概。"""
import re
import sys
from pathlib import Path

SRC = Path(r"E:\Projects\RenPy\Bring To Trial\game\script.rpy.orig")
DST = Path(r"E:\Projects\RenPy\BringToTrial-Demo\game\script.rpy")

CUT_MARK = "    # ========== 第二审：虚无 =========="

# (锚点：该行唯一子串, 图片名) —— 顺序即第一审的分镜顺序
SCENES = [
    ("怀着难以抑制的好奇与恐惧，少年蹀躞徐行", "art02_walk"),
    ("终于，在火光的尽头，他看见了那两个他既熟稔而又陌生的人", "art03_meet_sages"),
    ("其中一人身形高大，头顶微凹", "art04_confucius"),
    ("另一人的样貌普通平凡", "art05_west_sage"),
    ("少年大骇，因为他一眼便认出了前者", "art06_two_sages"),
    ("「他们那些胶柱鼓瑟的旧思想", "art07_sweet_smile"),
    ("为了审判你！", "art08_scholar"),
    ("在两位圣人身后的两侧分别走出了一位孔门儒生与一位苦行修士司祭", "art09_monk"),
    ("少年错愕不已，但很快又恢复了镇定", "art10_shock_to_smile"),
    ("少年感到诧异，心里陡地生起一股无名火", "art11_inner_anger"),
    ("你们既要审判我，那便来吧！无需装神弄鬼", "art12_disdain"),
    ("# 鲁鄹邑人三选一", "art13_choice_scholar"),
    ("# 加利利拿撒勒人三选一", "art14_choice_west"),
    ("少年放肆地笑道，眼里闪烁着轻蔑与挑衅", "art15_wild_laugh"),
    ("空口无凭，那你们在这方面的修为又如何", "art16_standoff"),
    ("少年沉思了一阵，他觉得自己理解得过于肤浅", "art17_realize"),
]

ART = ["art01_entry"] + [s[1] for s in SCENES]
IMAGE_DEFS = "\n".join('image %s = "art/%s.jpg"' % (a, a) for a in ART)

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
        tip = globals().get("CITAO_HOVER", {}).get(caption.strip("「」"), "")
        return tip or t("「%s」暂无阐释", "\\"%s\\": no note yet") % caption.strip("「」")

'''

SYNOPSIS_ZH = ("【故事梗概】\\n\\n"
               "铁门之内，那两位被亿万人顶礼膜拜的圣人——鲁鄹邑人与加利利拿撒勒人——正在等他。\\n"
               "少年不信他们那套旧道理，只想用自己时代的智慧把他们驳倒。\\n"
               "于是他等来的不是辩论，而是一场审判：先问物质，再问虚无，最后问那道谁也绕不开的道。\\n"
               "而自始至终，被审判的都是他自己。")

SYNOPSIS_EN = ("【Synopsis】\\n\\n"
               "Behind the iron gate, two men revered by countless millions — the Man of Zou and the Man of Nazareth — are waiting for him.\\n"
               "The youth does not believe a word of their old teaching, and means to refute them with the wisdom of his own age.\\n"
               "So what awaits him is not a debate but a trial: first materialism, then emptiness, and at last the one question no one can walk around.\\n"
               "And all along, he is the one on trial.")

SYNOPSIS = (
    '    # ========== 开场：黑屏故事梗概 ==========\n'
    '    scene black\n'
    '    $ line = t("%s", "%s")\n'
    '    centered "[line]"\n'
    '\n'
    '    scene art01_entry with fade'
) % (SYNOPSIS_ZH, SYNOPSIS_EN)

DEMO_END = '''    # ========== 试玩版到此结束 ==========
    scene black with fade
    $ line = t("—— 试玩版到此结束 ——\\n\\n少年还未迎上「第二审：虚无」。\\n\\n感谢游玩。", "—— End of the Demo ——\\n\\nThe Second Trial: Emptiness still awaits him.\\n\\nThank you for playing.")
    centered "[line]"
    return
'''

text = SRC.read_text(encoding="utf-8")
if CUT_MARK not in text:
    sys.exit("找不到第二审的切分注释，放弃")

body = text.split(CUT_MARK, 1)[0].rstrip() + "\n"

# ---- 去掉配音与配乐（演示版不带语音/音乐资源） ----
kept, removed = [], 0
for ln in body.split("\n"):
    if re.match(r'^\s*voice\s+"[^"]*"\s*$', ln) or re.match(r"^\s*(play|queue|stop)\s+\w+", ln):
        removed += 1
        continue
    kept.append(ln)
body = "\n".join(kept)

# ---- 按锚点插入分镜（开场那张另行处理） ----
lines = body.split("\n")
for anchor, img in SCENES:
    idx = [i for i, ln in enumerate(lines) if anchor in ln]
    if len(idx) != 1:
        sys.exit(f"锚点命中 {len(idx)} 次，需唯一：{anchor}")
    lines.insert(idx[0], f"    scene {img} with fade")
body = "\n".join(lines)

# ---- 开场：黑屏梗概 + 第一页 ----
if "    scene bg room with fade" not in body:
    sys.exit("找不到开场 scene bg room，放弃")
body = body.replace("    scene bg room with fade", SYNOPSIS, 1)

# ---- 选择菜单：简略词条 + 悬浮原文本 ----
expect_menus = body.count("\n    $ opt_a = ")
lines = body.split("\n")
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
body = "\n".join(out)
if menus != expect_menus:
    sys.exit(f"期望改写 {expect_menus} 个选择菜单，实际 {menus}")

# ---- 辅助函数与图片定义 ----
if body.count("# ---------- 角色定义 ----------") != 1:
    sys.exit("找不到角色定义段，放弃")
body = body.replace(
    "# ---------- 角色定义 ----------",
    HELPERS + "# ---------- 角色定义 ----------",
    1,
)
if body.count("label start:") != 1:
    sys.exit("label start 不唯一，放弃")
body = body.replace(
    "label start:",
    "# ---------- 演示版美术（豆包生成，覆盖第一审 第1-65页） ----------\n" + IMAGE_DEFS + "\n\nlabel start:",
    1,
)

body = body.rstrip() + "\n\n" + DEMO_END
DST.write_text(body, encoding="utf-8")

print(f"voice/audio 行移除: {removed}")
print(f"插入分镜: {len(SCENES)}")
print(f"改写选择菜单: {menus}")
print(f"演示版脚本行数: {len(body.splitlines())}")
