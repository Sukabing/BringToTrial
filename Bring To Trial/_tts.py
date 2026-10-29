# -*- coding: utf-8 -*-
"""从正式版 script.rpy 整理角色与配音清单，供 TTS 预设使用。

产出 docs/角色与配音清单.md、docs/voices.json、docs/voice_lines.csv
"""
import csv
import json
import re
from collections import Counter, OrderedDict
from pathlib import Path

PROJ = Path(r"E:\Projects\RenPy\Bring To Trial")
SCRIPT = PROJ / "game" / "script.rpy"
OUT = PROJ / "docs"

# 角色：say 变量 -> (中文名, 英文名, voice 前缀集合, TTS 设定)
ROLES = OrderedDict([
    ("narrator", dict(zh="旁白", en="Narrator",
                      prefixes=["vo_narr"],
                      voice="中性、低沉、冷静，近乎不带情绪的时间底色；语速偏慢，句尾不拖",
                      tts="中性男声或成熟女声皆可；rate 0.9；低情绪强度；不要角色化处理")),
    ("s", dict(zh="少年", en="Youth",
               prefixes=["vo_s"],
               voice="青年男声，二十上下，声线偏亮却发虚；傲慢时有轻挑的滑音，崩溃处带哭腔",
               tts="青年男声；rate 1.0；需要三档情绪：傲慢／犹疑／啜泣；避免卡通化")),
    ("lu", dict(zh="鲁鄹邑人（孔子）", en="Man of Zou",
                prefixes=["vo_lu", "vo_lu_mat", "vo_lu_emp", "vo_lu_root", "vo_lu_amd", "vo_lu_end"],
                voice="长者男声，温厚沉稳，诵经典时气息绵长、字字落地；不激昂",
                tts="老年男声；rate 0.85；强度低，句中停顿可略长；引用经典时保持同一语气")),
    ("ga", dict(zh="加利利拿撒勒人（耶稣）", en="Man of Nazareth",
                prefixes=["vo_ga", "vo_ga_mat", "vo_ga_emp", "vo_ga_root", "vo_ga_amd", "vo_ga_end"],
                voice="中年男声，音量不高但有穿透，带一点疲惫后的温柔；不煽情",
                tts="中年男声；rate 0.9；轻声但不虚弱；避免布道腔")),
    ("conf", dict(zh="孔门儒生", en="Confucian Scholar",
                  prefixes=["vo_conf", "vo_conf_mat", "vo_conf_emp", "vo_conf_ver"],
                  voice="壮年男声，清正、方正、字正腔圆，语调平直少起伏",
                  tts="壮年男声；rate 1.0；咬字清晰；情绪恒定")),
    ("monk", dict(zh="苦行修士司祭", en="Ascetic Monk Priest",
                  prefixes=["vo_monk", "vo_monk_mat", "vo_monk_emp", "vo_monk_ver"],
                  voice="中老年男声，嗓音粗粝微沙，带诵经的韵律感",
                  tts="老年男声；rate 0.85；轻微沙哑与气声；诵经句可加长尾")),
    ("unknown", dict(zh="未知声音（未见其形）", en="Unknown Voice",
                     prefixes=["vo_unknown"],
                     voice="开场两位圣人只闻其声时的念诵，低沉、远、带空间感",
                     tts="lu 与 ga 声线各一遍叠录，或用第三条男声；加混响；rate 0.85")),
    ("other", dict(zh="另一个自己", en="The Other Self",
                   prefixes=["vo_other"],
                   voice="少年自己的另一个我：同一声线的低八度版本，平静且不容置疑",
                   tts="少年声线降调 2~3 半音，加轻微混响；rate 0.85；不带情绪")),
])

SPEAKER_ALIASES = {"narrator": "narrator", "s": "s", "lu": "lu", "ga": "ga",
                   "conf": "conf", "monk": "monk", "unknown": "unknown", "other": "other"}


def parse():
    lines = SCRIPT.read_text(encoding="utf-8").split("\n")
    rows, pending, pending_prefix = [], [], ""
    i = 0
    while i < len(lines):
        mv = re.match(r'\s+voice "([^"]+)"', lines[i])
        if mv:
            pending.append(mv.group(1))
            i += 1
            continue
        ml = re.match(r'\s+\$ line = t\("((?:[^"\\]|\\.)*)", "((?:[^"\\]|\\.)*)"\)', lines[i])
        if ml and pending:
            speaker = None
            for j in range(i + 1, min(i + 4, len(lines))):
                ms = re.match(r'\s+(\w+) "\[line\]"', lines[j])
                if ms:
                    speaker = ms.group(1)
                    break
            for vid in pending:
                rows.append(dict(voice=vid, speaker=speaker or "narrator",
                                 zh=ml.group(1), en=ml.group(2)))
            pending = []
        elif re.match(r'\s+\w+ "\[line\]"', lines[i]):
            pending = []
        i += 1
    return rows


rows = parse()
by_role = Counter(r["speaker"] for r in rows)
prefix_counts = Counter(r["voice"].rsplit("_", 1)[0] for r in rows)

OUT.mkdir(exist_ok=True)

# ---- CSV（UTF-8 BOM，Excel 直接开） ----
with (OUT / "voice_lines.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["voice_id", "角色变量", "角色", "中文台词", "英文台词"])
    for r in rows:
        role = ROLES.get(r["speaker"], {})
        w.writerow([r["voice"], r["speaker"], role.get("zh", r["speaker"]), r["zh"], r["en"]])

# ---- JSON 预设骨架 ----
presets = []
for key, info in ROLES.items():
    sample = next((r for r in rows if r["speaker"] == key), None)
    presets.append({
        "id": key,
        "name_zh": info["zh"],
        "name_en": info["en"],
        "voice_prefixes": info["prefixes"],
        "line_count": by_role.get(key, 0),
        "voice_direction": info["voice"],
        "tts_hint": info["tts"],
        "gender": {"narrator": "any", "s": "male", "lu": "male", "ga": "male",
                   "conf": "male", "monk": "male", "unknown": "male", "other": "male"}[key],
        "age": {"narrator": "adult", "s": "young", "lu": "elder", "ga": "middle",
                "conf": "middle", "monk": "elder", "unknown": "elder", "other": "young"}[key],
        "rate": {"narrator": 0.9, "s": 1.0, "lu": 0.85, "ga": 0.9,
                 "conf": 1.0, "monk": 0.85, "unknown": 0.85, "other": 0.85}[key],
        "emotion_presets": {
            "s": ["傲慢", "犹疑", "啜泣"],
            "monk": ["诵经", "劝诫"],
            "lu": ["温厚", "断语"],
            "ga": ["平和", "劝诫"],
        }.get(key, []),
        "reference_line_zh": sample["zh"] if sample else "",
        "reference_line_en": sample["en"] if sample else "",
        "reference_voice_file": sample["voice"] if sample else "",
    })
(OUT / "voices.json").write_text(json.dumps(presets, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")

# ---- Markdown 清单 ----
md = []
md.append("# 《三审少年》角色与配音清单\n")
md.append(f"脚本：`game/script.rpy`　配音行合计 **{len(rows)}** 条\n")
md.append("## 角色总表\n")
md.append("| 角色 | voice 前缀 | 条数 | 音色方向 | TTS 建议 |")
md.append("| --- | --- | ---: | --- | --- |")
for key, info in ROLES.items():
    total = by_role.get(key, 0)
    if not total:
        continue
    md.append(f"| {info['zh']} | `{info['prefixes'][0]}_*` | {total} | {info['voice']} | {info['tts']} |")
md.append("")
md.append("## 分前缀条数\n")
md.append("| voice 前缀 | 条数 |")
md.append("| --- | ---: |")
for p, c in sorted(prefix_counts.items(), key=lambda kv: (-kv[1], kv[0])):
    md.append(f"| `{p}` | {c} |")
md.append("")
md.append("## 预设记录表（填好后回填 voices.json）\n")
md.append("| 角色 | 参考声线/模型 | 语速 | 音高偏移 | 情绪标签 | 备注 |")
md.append("| --- | --- | --- | --- | --- | --- |")
for key, info in ROLES.items():
    if not by_role.get(key):
        continue
    md.append(f"| {info['zh']} |  |  |  |  |  |")
md.append("")
md.append("## 需要注意的两处\n")
md.append("1. `vo_conf_001.ogg` 与 `vo_monk_001.ogg` 同属一句「为了审判你！」——儒生与修士齐声，剧本里落在 `conf` 行。若要分开配，需拆成两句。")
md.append("2. `vo_lu_end.ogg` / `vo_ga_end.ogg` 是结局的临别寄语，声线应与全篇的 `vo_lu_*` / `vo_ga_*` 完全一致，不要换版本。")
md.append("")
md.append("## 逐条台词\n")
md.append("见 `voice_lines.csv`（voice_id / 角色 / 中文 / 英文），可直接喂给批量 TTS。")
(OUT / "角色与配音清单.md").write_text("\n".join(md) + "\n", encoding="utf-8")

print(f"配音行 {len(rows)} 条，角色 {len([k for k in ROLES if by_role.get(k)])} 个")
for k, info in ROLES.items():
    print(f"  {info['zh']:<12} {by_role.get(k, 0):>3}")
print(f"-> {OUT}\\角色与配音清单.md")
print(f"-> {OUT}\\voices.json")
print(f"-> {OUT}\\voice_lines.csv")
