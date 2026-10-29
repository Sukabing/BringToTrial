# -*- coding: utf-8 -*-
"""从「词条阐释.docx」抽选择支词条的解释，生成工程的 game/citao.rpy。

hover 面板用的就是这份：出处 + 核心思想；没有分字段的条目直接取标题下的整段解释。

用法: python _citao.py "<工程目录>"
"""
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX = Path(r"E:\SCNU\课程任务\ai跨界写作\词条阐释.docx")
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# 剧本里的词条名与文档标题不一致的，在这里对齐
ALIASES = {"乡愿之辩": "乡原之辩", "磐石之屋": "屋矗立磐石之上"}

FIELDS = ("出处：", "原文：", "翻译：", "注释：", "核心思想：",
          "文学化用：", "意义上的新解释：", "陀思妥耶夫斯基如何应用：")


def doc_paragraphs(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    lines = []
    for child in body:
        if child.tag.split("}")[-1] == "p":
            parts = []
            for node in child.iter():
                t = node.tag.split("}")[-1]
                if t == "t" and node.text:
                    parts.append(node.text)
                elif t == "br":
                    parts.append("\n")
            lines.append("".join(parts))
    return lines


def parse_entries(lines):
    text = "\n".join(lines)
    blocks = [b.strip() for b in re.split(r"\n\n+", text) if b.strip()]
    entries, cur = {}, None
    for b in blocks:
        first = b.split("\n")[0].strip()
        m = re.search(r"[“\"]([^”\"]{1,12})[”\"]", first)
        name = m.group(1).strip() if m else None
        if cur is not None and any(first.startswith(f) for f in FIELDS):
            entries[cur] += "\n" + b
        elif name:
            cur = name
            entries[cur] = b
        else:
            cur = None
    return entries


def build_hover(entry):
    """取一条词条里最适合给玩家看的部分：出处 + 核心思想；没有就整段。"""
    lines = [l.strip() for l in entry.split("\n") if l.strip()]
    title, body = lines[0], lines[1:]
    src = next((l for l in body if l.startswith("出处：")), "")
    core = next((l for l in body if l.startswith("核心思想：")), "")
    if core:
        return "\n".join(x for x in (src, core) if x)
    rest = "".join(body).strip()
    if rest:
        return rest
    # 标题与解释挤在同一行的条目：去掉「“词条”（出处）：」前缀，剩下就是解释
    return re.sub(r'^[“"][^”"]{1,12}[”"]\s*(（[^）]*）)?\s*[：:]\s*', "", title).strip()


def script_tags(script: Path):
    text = script.read_text(encoding="utf-8")
    tags = []
    for m in re.finditer(r'\$ opt_[abc] = t\("聆听「(.+?)」"', text):
        if m.group(1) not in tags:
            tags.append(m.group(1))
    return tags


def main():
    if len(sys.argv) < 2:
        sys.exit('用法: python _citao.py "<工程目录>"')
    project = Path(sys.argv[1])
    tags = script_tags(project / "game" / "script.rpy")
    entries = parse_entries(doc_paragraphs(DOCX))

    found, missing = [], []
    for t in tags:
        key = ALIASES.get(t, t)
        (found if key in entries else missing).append((t, key))

    out = ['# 本文件由 _citao.py 从「词条阐释.docx」自动生成，勿手改。',
           '# 键是菜单上的简略词条，值是鼠标悬浮时显示的阐释。',
           'init python:',
           '    CITAO_HOVER = {}',
           '']
    for t, key in found:
        out.append(f'    CITAO_HOVER[{json.dumps(t, ensure_ascii=False)}] = '
                   f'{json.dumps(build_hover(entries[key]), ensure_ascii=False)}')
        out.append('')
    (project / "game" / "citao.rpy").write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"[{project.name}] 词条 {len(tags)} 个，命中 {len(found)} 个")
    if missing:
        print(f"  文档缺: {'、'.join(t for t, _ in missing)}")
    for t, key in found:
        note = f"（改用「{key}」）" if key != t else ""
        print(f"  ✓ {t}{note}  {len(build_hover(entries[key]))} 字")
    if not found:
        sys.exit("一个都没匹配上")


if __name__ == "__main__":
    main()
