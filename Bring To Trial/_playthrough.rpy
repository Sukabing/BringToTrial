testsuite global:
    before testcase:
        $ _test.transition_timeout = 0.05
        $ _test.timeout = 2.0

        if not screen "main_menu":
            run MainMenu(confirm=False)

    teardown:
        exit

testcase full_playthrough:
    assert screen "main_menu"
    click "开始游戏"
    advance until screen "choice"
    click "中文"
    advance until "故事梗概"
    advance until screen "choice"
    click "「德本财末」"
    advance until screen "choice"
    click "「天上之财宝」"
    advance until screen "choice"
    click "「陈蔡绝粮」"
    advance until screen "choice"
    click "「旷野三试」"
    advance until screen "choice"
    click "「乡愿之辩」"
    advance until screen "choice"
    click "「温水灵魂」"
    advance until screen "choice"
    click "「大丈夫」"
    advance until screen "choice"
    click "「磐石之屋」"
    advance until screen "choice"
    click "「失民则亡」"
    advance until screen "choice"
    click "「葡萄树与枝子」"
    advance until screen "choice"
    click "「晋公知过」"
    advance until screen "choice"
    click "「拉撒路复活」"
    advance until screen "choice"
    click "「诚其意毋自欺」"
    advance until screen "choice"
    click "「格拉森群鬼」"
    advance until screen "main_menu"
