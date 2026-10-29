testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 2.0

        if not screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit

## 回归测试：真的把鼠标挪到选项上，确认说明条换成了该词条的阐释。
## 曾经因为菜单 caption 还是 "[tag_a]"（未插值）而永远查不到词条，这条能抓住。
testcase hover_probe:
    click "开始游戏"
    advance until screen "choice"
    click "中文"
    advance until "故事梗概"
    advance until screen "choice"

    $ import renpy.test.testmouse as tm
    $ print("PROBE start =", repr(menu_tip))

    $ tm.move_mouse(960, 312)
    pause 0.6
    $ print("PROBE hover#1 =", repr(menu_tip)[:70])
    $ assert menu_tip.startswith("出处："), menu_tip

    $ tm.move_mouse(960, 498)
    pause 0.6
    $ print("PROBE hover#3 =", repr(menu_tip)[:70])
    $ assert menu_tip.startswith("出处："), menu_tip

    $ tm.move_mouse(960, 1000)
    pause 0.6
    $ print("PROBE leave =", repr(menu_tip))
    $ assert menu_tip == "", menu_tip
