# 版本管理速查（Ren'Py 三审少年）

仓库根目录：`E:\Projects\RenPy`　分支：`main`

## 现在有什么

```text
98612f4  初始提交：三审少年（正式版 + 演示版）
89a6bf6  选择支下方改为常驻说明条：默认显示提示语，悬停换成该词条的阐释
```

## 常用回退

```bash
cd E:\Projects\RenPy

git log --oneline                 # 看历史
git show 98612f4 --stat           # 看某次提交动了哪些文件

# 只回退一个文件到某个版本（不碰其他文件，最安全）
git restore --source=98612f4 -- "Bring To Trial/game/screens.rpy"

# 整体回到某个版本（丢弃之后所有改动，先确认工作区干净）
git reset --hard 98612f4

# 撤销还没提交的改动
git restore -- "Bring To Trial/game/script.rpy"

# 先存个岔路再改（推荐：改之前打个分支）
git tag before-xxx
```

## 没入库的东西

| 路径 | 原因 |
| --- | --- |
| `BringToTrial-Demo-dists/` | 打包产物，随时可重打 |
| `美术资源（豆包/` | 原图约 85 MB，转换后的成品在 `game/art/` 已入库 |
| `game/saves/`、`game/cache/`、`*.rpyc` | Ren'Py 运行时生成 |
| `log.txt`、`errors.txt`、`traceback.txt` | 运行日志 |

## 重新生成脚本

```bash
# 正式版（改完 script.rpy.orig 或美术后）
python "Bring To Trial\_assets_full.py"
python "Bring To Trial\_full.py"
python "Bring To Trial\_patch_full.py"    # 仅首次：screens/options/gui 打补丁
python "Bring To Trial\_citao.py" "E:\Projects\RenPy\Bring To Trial"
python "Bring To Trial\_tts.py"

# 演示版：沿用正式版的 screens/gui，脚本从 script.rpy.orig 裁切生成
python "BringToTrial-Demo\_patch.py"
python "BringToTrial-Demo\_script.py"
python "Bring To Trial\_citao.py" "E:\Projects\RenPy\BringToTrial-Demo"
```

打包演示版：

```bash
"E:\Apps\renpy-8.5.3-sdk\lib\py3-windows-x86_64\python.exe" `
  "E:\Apps\renpy-8.5.3-sdk\renpy.py" "E:\Apps\renpy-8.5.3-sdk\launcher" `
  distribute "E:\Projects\RenPy\BringToTrial-Demo" --dest "E:\Projects\RenPy\BringToTrial-Demo-dists" --package pc
```
