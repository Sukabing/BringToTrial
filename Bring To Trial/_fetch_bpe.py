# -*- coding: utf-8 -*-
"""从 ModelScope 补下 IndexTTS-2 缺的 bpe.model（只有几百 KB，不用整包 5GB）。"""
import sys
from pathlib import Path

CKPT = Path(r"E:\index-tts\checkpoints")
TARGET = CKPT / "bpe.model"

if TARGET.exists():
    print(f"已存在: {TARGET} ({TARGET.stat().st_size} B)")
    sys.exit(0)

from modelscope.hub.file_download import model_file_download

for file_path in ("bpe.model", "checkpoints/bpe.model"):
    try:
        got = model_file_download(model_id="IndexTeam/IndexTTS-2", file_path=file_path,
                                  local_dir=str(CKPT))
        print(f"下载成功: {file_path} -> {got}")
        src = Path(got)
        if src.resolve() != TARGET.resolve():
            TARGET.write_bytes(src.read_bytes())
            print(f"已复制到 {TARGET}")
        break
    except Exception as exc:  # noqa: BLE001
        print(f"{file_path} 失败: {type(exc).__name__}: {exc}")

print("结果:", TARGET.exists(), TARGET.stat().st_size if TARGET.exists() else "")
