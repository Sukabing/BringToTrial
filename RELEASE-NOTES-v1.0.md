# Bring To Trial · 三审少年 `v1.0`

铁门之内，两位被亿万人顶礼膜拜的圣人——鲁鄹邑人与加利利拿撒勒人——在等他。
少年不信他们那套旧道理，只想用自己时代的智慧把他们驳倒。
于是他等来的不是辩论，而是一场审判：先问物质，再问虚无，最后问那道谁也绕不开的根基。
而自始至终，被审判的都是他自己。

## 这一版变了什么

- **坏结局收尾换了专属美术**：最后那一幕「纵身朝远处混沌的黑暗中奔去」，原本和正式结局共用同一张旷野图，现在换成《奔向黑暗》。
- 坏结局配音 `vo_bad_001`–`vo_bad_024` 与 BGM 全部随包发出，不再缺音。
- 发行包里不再夹带开发备份脚本（`script.rpy.bak`）。

## 内容

- 371 段对话、15 处选择、34 张分镜，全程配音
- 中英双语（开局选一次，随时可在设置里切换）
- 三次审判：物质 → 虚无 → 根基；怎么答，决定你落在哪个结局
- Ren'Py 8.5.3

## 安装

1. 下载下面的 `BringToTrial-1.0-pc.zip`（约 166 MB）
2. 解压到任意目录
3. 双击 `BringToTrial.exe`

Windows 10 / 11 x64。首次运行若提示「未知发布者」，是因为安装包没有签名，选「仍要运行」即可。

## 校验

```text
SHA256  0A147481C0DFD71D7DB938248466B41241CD07F7B9DCB9775932C38B51AD511B
```

## 从源码重跑

```text
python "_assets_full.py"     # 美术资源 → game/art/*.jpg（1920x1080）
python "_full.py"            # 补分镜/词条/字号函数/坏结局配图
python "_e2e.ps1"            # 全流程自动通关测试
```

打开发行包：

```powershell
& "E:\Apps\renpy-8.5.3-sdk\lib\py3-windows-x86_64\python.exe" `
  "E:\Apps\renpy-8.5.3-sdk\renpy.py" "E:\Apps\renpy-8.5.3-sdk\launcher" `
  distribute "E:\Projects\RenPy\Bring To Trial" `
  --dest "E:\Projects\RenPy\BringToTrial-1.0-dists" --package pc
```
