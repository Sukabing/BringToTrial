# 三审少年 - 完整可运行版
# 支持中英双语切换 / 全配音占位 / 全选择分支

init python:
    # 默认语言持久化存储
    if not persistent.lang:
        persistent.lang = "zh"

    # 双语翻译函数
    def t(zh, en):
        if persistent.lang == "zh":
            return zh
        else:
            return en

default menu_tip = ""
# 三审各自记错：每审选错达到一半，该审判为 ♦
default wrong_material = 0
default wrong_emptiness = 0
default wrong_root = 0
default win_material = 0
default win_emptiness = 0
default win_root = 0
default wins = 0
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
        return tip or t("「%s」暂无阐释", "\"%s\": no note yet") % caption.strip("「」")

# ---------- 配音侧链：voice 通道一响，背景音乐自动压下去 ----------
default _ducking = False

init python:
    DUCK_VOLUME = 0.35     # 有配音时 music 的增益
    DUCK_FADE_IN = 0.25    # 压下去的时长（秒）
    DUCK_FADE_OUT = 0.60   # 放回来的时长（秒）

    def _duck_poll():
        playing = renpy.music.get_playing("voice") is not None
        if playing == globals().get("_ducking", False):
            return
        globals()["_ducking"] = playing
        renpy.music.set_volume(
            DUCK_VOLUME if playing else 1.0,
            DUCK_FADE_IN if playing else DUCK_FADE_OUT,
            channel="music",
        )

    config.periodic_callbacks.append(_duck_poll)

# ---------- 角色定义 ----------
define narrator = Character(None)
define s = Character("[s_name]", color="#cccccc")
define lu = Character("[lu_name]", color="#d4a574")
define ga = Character("[ga_name]", color="#87ceeb")
define conf = Character("[conf_name]", color="#c9a86c")
define monk = Character("[monk_name]", color="#93b7e3")
define unknown = Character("???", color="#888888")
define other = Character("[other_name]", color="#e0b0ff")

# ---------- 美术资源（豆包生成，第1-122页） ----------
image art01_entry = "art/art01_entry.jpg"
image art02_walk = "art/art02_walk.jpg"
image art03_meet_sages = "art/art03_meet_sages.jpg"
image art04_confucius = "art/art04_confucius.jpg"
image art05_west_sage = "art/art05_west_sage.jpg"
image art06_two_sages = "art/art06_two_sages.jpg"
image art07_sweet_smile = "art/art07_sweet_smile.jpg"
image art08_scholar = "art/art08_scholar.jpg"
image art09_monk = "art/art09_monk.jpg"
image art10_shock_to_smile = "art/art10_shock_to_smile.jpg"
image art11_inner_anger = "art/art11_inner_anger.jpg"
image art12_disdain = "art/art12_disdain.jpg"
image art13_choice_scholar = "art/art13_choice_scholar.jpg"
image art14_choice_west = "art/art14_choice_west.jpg"
image art15_wild_laugh = "art/art15_wild_laugh.jpg"
image art16_standoff = "art/art16_standoff.jpg"
image art17_realize = "art/art17_realize.jpg"
image art18_gloomy = "art/art18_gloomy.jpg"
image art19_choice3 = "art/art19_choice3.jpg"
image art20_choice4 = "art/art20_choice4.jpg"
image art21_struggle = "art/art21_struggle.jpg"
image art22_look_at_them = "art/art22_look_at_them.jpg"
image art23_despair = "art/art23_despair.jpg"
image art24_choice5 = "art/art24_choice5.jpg"
image art25_choice6 = "art/art25_choice6.jpg"
image art26_look_up = "art/art26_look_up.jpg"
image art27_walk_out = "art/art27_walk_out.jpg"
image art28_face_to_face = "art/art28_face_to_face.jpg"
image art29_choice7 = "art/art29_choice7.jpg"
image art30_ask = "art/art30_ask.jpg"
image art31_leave = "art/art31_leave.jpg"
image art32_look_back = "art/art32_look_back.jpg"
image art33_field = "art/art33_field.jpg"
image art34_run_dark = "art/art34_run_dark.jpg"

label start:
    # 语言选择
    menu:
        "中文":
            $ persistent.lang = "zh"
        "English":
            $ persistent.lang = "en"

    # 根据语言设置角色名
    if persistent.lang == "zh":
        $ s_name = "少年"
        $ lu_name = "鲁鄹邑人"
        $ ga_name = "加利利拿撒勒人"
        $ conf_name = "孔门儒生"
        $ monk_name = "苦行修士司祭"
        $ other_name = "少年"
    else:
        $ s_name = "Youth"
        $ lu_name = "Man of Zou"
        $ ga_name = "Man of Nazareth"
        $ conf_name = "Confucian Scholar"
        $ monk_name = "Ascetic Monk Priest"
        $ other_name = "Youth"

    # ========== 开场：黑屏故事梗概 ==========
    scene black
    # 台本开头的引入
    $ line = t("这是一个发生在我们同时代的关于少年受审的故事，也是一个少年破除执迷、重获新生的故事。", "This is a tale set in our own times, of a youth put on trial, and of one who casts off his obsessions to win a new-found life.")
    centered "[line]"

    $ line = t("【故事梗概】\n\n铁门之内，那两位被亿万人顶礼膜拜的圣人——鲁鄹邑人与加利利拿撒勒人——正在等他。\n少年不信他们那套旧道理，只想用自己时代的智慧把他们驳倒。\n于是他等来的不是辩论，而是一场审判：先问物质，再问虚无，最后问那道谁也绕不开的根基。\n而自始至终，被审判的都是他自己。", "【Synopsis】\n\nBehind the iron gate, two men revered by countless millions — the Man of Zou and the Man of Nazareth — are waiting for him.\nThe youth does not believe a word of their old teaching, and means to refute them with the wisdom of his own age.\nSo what awaits him is not a debate but a trial: first materialism, then emptiness, and at last the root no one can walk around.\nAnd all along, he is the one on trial.")
    centered "[line]"

    scene art01_entry with fade
    ## 背景音乐：game/audio/bgm.ogg（bg.wav 转码，194 秒；主菜单同一首，已在播就不重启）
    $ renpy.music.play("audio/bgm.ogg", if_changed=True, fadein=2.0)

    # ========== 开场 ==========
    voice "vo_narr_001.ogg"
    $ line = t("少年推开那座沉重的铁门，屋内磬静的黢黑刹时吞噬了他那渺小的身躯。", "The youth pushed open the heavy iron gate, and the profound, silent darkness within swallowed his frail frame in an instant.")
    narrator "[line]"

    voice "vo_narr_002.ogg"
    $ line = t("少年眯起双眼，极力想看清屋内的情状，但除了远处的几朵飘忽不定的幽火以外，其余的一切全被漆上了一层浓稠的黑。", "He narrowed his eyes, straining to make out the interior. Yet save for a few wandering, ghostly flames flickering in the distance, all else was drowned in a thick, viscous gloom.")
    narrator "[line]"

    voice "vo_narr_003.ogg"
    scene art02_walk with fade
    $ line = t("怀着难以抑制的好奇与恐惧，少年蹀躞徐行，向远处揜菼的灯火趋近。", "Driven by a mingled thrill of curiosity and dread, he paced slowly forward, stepping softly toward the distant, wavering light.")
    narrator "[line]"

    voice "vo_narr_004.ogg"
    $ line = t("倏忽，他听到了两个浑厚沉雄的声音。起初声音微渺，时断时续。少年停步，侧耳细听：", "Suddenly, two deep, sonorous voices reached his ears. At first they were faint, broken and intermittent. He halted, tilting his head to listen more closely:")
    narrator "[line]"

    voice "vo_unknown_001.ogg"
    $ line = t("世衰道微，邪说暴行有作，臣弑其君者有之，子弑其父者有之。", "When the world declined, and true principles fell into disuse, perverse doctrines and violent deeds arose. There were instances of ministers murdering their sovereigns, and sons murdering their fathers.")
    unknown "[line]"

    voice "vo_unknown_002.ogg"
    $ line = t("邪说诬民，充塞仁义也。仁义充塞，则率兽食人，人将相食。吾为此惧，闲先圣之道，距杨墨，放淫辞，邪说者不得作。", "Such perverse doctrines delude the people, and block up the path of benevolence and righteousness. When benevolence and righteousness are thus blocked up, it is as if men were leading beasts to devour men, and they will be found devouring one another. I am alarmed at these things, and therefore defend the ways of the ancient sages, opposing Yang and Mo, and setting aside licentious speeches.")
    unknown "[line]"

    voice "vo_unknown_003.ogg"
    $ line = t("作于其心，害于其事；作于其事，害于其政。圣人复起，不易吾言矣。", "What arises in the mind, works injuriously on affairs; what works injuriously on affairs, works injuriously on government. Were a sage to arise again, he would not change my words.")
    unknown "[line]"

    voice "vo_unknown_004.ogg"
    $ line = t("第三位天使吹号，就有烧着的大星，好像火把从天上落下来，落在江河的三分之一和众水的泉源上。", "And the third angel sounded, and there fell a great star from heaven, burning as it were a lamp, and it fell upon the third part of the rivers, and upon the fountains of waters;")
    unknown "[line]"

    voice "vo_unknown_005.ogg"
    $ line = t("这星名叫「茵陈」。众水的三分之一变为茵陈；因水变苦，就死了许多人。", "And the name of the star is called Wormwood: and the third part of the waters became wormwood; and many men died of the waters, because they were made bitter.")
    unknown "[line]"

    voice "vo_narr_005.ogg"
    $ line = t("谈话声音戛然而止。少年覃思罔悟，对刚才谈话的二人及其言语愈发感到好奇，便加快步调向那灯火处走去。", "The voices ceased abruptly. Puzzled and increasingly curious about the two speakers and their words, the youth quickened his pace toward the light.")
    narrator "[line]"

    voice "vo_narr_006.ogg"
    scene art03_meet_sages with fade
    $ line = t("终于，在火光的尽头，他看见了那两个他既熟稔而又陌生的人：", "At last, at the end of the glow, he beheld the two figures, at once familiar and strange to him:")
    narrator "[line]"

    voice "vo_narr_007.ogg"
    scene art04_confucius with fade
    $ line = t("其中一人身形高大，头顶微凹，面容庄重，衣饰朴素，带有几分栉风沐雨的憔悴感；", "One was tall of stature, with a slightly sunken crown, a solemn countenance, and plain robes, bearing the weariness of one who had journeyed far and endured much.")
    narrator "[line]"

    voice "vo_narr_008.ogg"
    scene art05_west_sage with fade
    $ line = t("另一人的样貌普通平凡，无夺目美貌，但神色柔和而坚定，脸上显出一种饱经风霜的质感。", "The other was of common, unremarkable appearance, with no striking beauty, yet his gaze was gentle and steadfast, his face marked with the texture of a life seasoned by trials.")
    narrator "[line]"

    voice "vo_narr_009.ogg"
    scene art06_two_sages with fade
    $ line = t("少年大骇，因为他一眼便认出了前者正是那鲁鄹邑人，而后者则是加利利拿撒勒人。", "The youth started, for he recognized at once the former as the Man of Zou from Lu, and the latter as the Man of Nazareth from Galilee.")
    narrator "[line]"

    voice "vo_narr_010.ogg"
    $ line = t("「他们在这里干嘛呢？」少年心想，但不知为何，他油然生出了一种乖戾的想法：", "\"What are they doing here?\" he thought. Yet for some reason, a perverse notion rose within him:")
    narrator "[line]"

    voice "vo_narr_011.ogg"
    $ line = t("他想用自己的智慧驳倒这两位德高年劭、被芸芸众生顶礼膜拜的圣人。", "he would use his own wits to refute these two sages, revered and worshipped by multitudes.")
    narrator "[line]"

    voice "vo_narr_012.ogg"
    scene art07_sweet_smile with fade
    $ line = t("「他们那些胶柱鼓瑟的旧思想怎么能胜过我们的新思想呢？」少年露出一丝甜腻腻的微笑，迈步向他们走去。", "\"How can their rigid, outdated old ideas ever prevail against the thinking of our time?\" A faint, smug smile tugged at his lips as he stepped toward them.")
    narrator "[line]"

    voice "vo_s_001.ogg"
    $ line = t("喂，那个鄹邑的，还有那个加利利的，你们在这干嘛？", "Ho there, you of Zou, and you of Galilee. What are you doing here?")
    s "[line]"

    voice "vo_narr_013.ogg"
    $ line = t("少年强装出一副恭维的笑容，尽管他知道他那放荡无理的言语已经无法掩盖他那鬼迷心窍的意志了。", "he called, forcing a smile of feigned deference, though he knew his reckless, insolent words could no longer hide his defiant, mischief-bound resolve.")
    narrator "[line]"

    voice "vo_conf_001.ogg"
    voice "vo_monk_001.ogg"
    scene art08_scholar with fade
    $ line = t("为了审判你！", "To judge you!")
    conf "[line]"

    voice "vo_narr_014.ogg"
    scene art09_monk with fade
    $ line = t("在两位圣人身后的两侧分别走出了一位孔门儒生与一位苦行修士司祭，他们神色凛然，异口同声地说道。", "From either side behind the two sages stepped forth a Confucian Scholar and an Ascetic Monk Priest, their countenances stern, speaking as one.")
    narrator "[line]"

    voice "vo_s_002.ogg"
    $ line = t("审判…我？", "Judge… me?")
    s "[line]"

    voice "vo_narr_015.ogg"
    scene art10_shock_to_smile with fade
    $ line = t("少年错愕不已，但很快又恢复了镇定，脸上又重现出他方才糊上的笑。", "The youth was taken aback, but quickly recovered his composure, the earlier smile returning to his face.")
    narrator "[line]"

    voice "vo_s_003.ogg"
    $ line = t("你们凭何来审判我，我何罪之有？", "By what right do you judge me? What sin have I committed?")
    s "[line]"

    voice "vo_narr_016.ogg"
    $ line = t("他歪着脑袋，详装思索，抹了露出一层哂意：", "He tilted his head, feigning thought, a flicker of mockery playing across his features.")
    narrator "[line]"

    voice "vo_s_004.ogg"
    $ line = t("是因为我没能践行你们儒家的准则呢，还是因为我不信基督？", "Is it that I have failed to live by your Confucian rules? Or because I do not believe in Christ?")
    s "[line]"

    voice "vo_narr_017.ogg"
    $ line = t("两位圣贤正襟危坐，一言不发；从他们身后走到侧旁的孔门儒生与苦行修士司祭也正色凛然地望着他。", "The two sages sat upright and silent, while the Confucian Scholar and the Ascetic Monk Priest, having stepped to their sides, gazed at him with solemn gravity.")
    narrator "[line]"

    voice "vo_narr_018.ogg"
    scene art11_inner_anger with fade
    $ line = t("少年感到诧异，心里陡地生起一股无名火：", "The youth, surprised, felt a surge of unprovoked anger rise in his chest.")
    narrator "[line]"

    voice "vo_s_005.ogg"
    scene art12_disdain with fade
    $ line = t("你们既要审判我，那便来吧！无需装神弄鬼，法官们。", "If you mean to judge me, then get on with it! No need for all this mystic posturing, judges.")
    s "[line]"

    # ========== 第一审：物质 ==========
    voice "vo_narr_019.ogg"
    $ line = t("—— 第一审：物质 ——", "—— First Trial: Materialism ——")
    narrator "[line]"

    voice "vo_s_006.ogg"
    $ line = t("说我物质？你们难道不是在空谈道义？", "You call me materialistic? Is it not you who prattle on empty about morality and virtue?")
    s "[line]"

    voice "vo_s_007.ogg"
    $ line = t("没有果腹的食粮，人连立身都难，还谈什么精神操守？", "Without bread to fill the belly, a man can scarce stand on his own two feet—what use are spiritual principles then?")
    s "[line]"

    voice "vo_s_008.ogg"
    $ line = t("整个社会都在看重利益、讲求实效，我又有何不对之处？", "The whole world prizes profit and results. What wrong is there in that?")
    s "[line]"

    voice "vo_s_009.ogg"
    $ line = t("这世道波诡云谲，惟物质才是底气，惟钱财才有选择。", "In this treacherous, shifting world, only substance gives security, only wealth gives choice.")
    s "[line]"

    voice "vo_s_010.ogg"
    $ line = t("你们所谓的德行仁义、安贫乐道，你们所谓的甚于面包的石头岂能饱食终日，能遮风挡雨吗？", "Can your so-called virtue and benevolence, your praise of poverty and contentment—can your stones that are more than bread ever fill a stomach, or shelter a man from the wind and rain?")
    s "[line]"

    voice "vo_s_011.ogg"
    $ line = t("与其抱着空原则受苦受穷，不如凭本事挣来实打实的好日子。", "Rather than cling to empty principles and suffer in poverty, I would earn a solid, tangible good life by my own ability.")
    s "[line]"

    voice "vo_s_012.ogg"
    $ line = t("人往高处走，逐利本就天经地义，追寻物质何罪之有？", "Every man strives for better things. The pursuit of profit is only natural. What sin is there in seeking material comfort?")
    s "[line]"

    scene art13_choice_scholar with fade
    # 鲁鄹邑人三选一
    $ opt_a = t("聆听「德本财末」", "Hear: The Root of Virtue")
    $ opt_b = t("聆听「义利之警」", "Hear: Warning Against Profit")
    $ opt_c = t("聆听「生财之道」", "Hear: The Way of Wealth")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump lu_material_a
        "[tag_b]":
            $ wrong_material += 1
            jump lu_material_b
        "[tag_c]":
            $ wrong_material += 1
            jump lu_material_c

label lu_material_a:
    voice "vo_lu_mat_a.ogg"
    $ line = t("君子先慎乎德。有德此有人，有人此有土，有土此有财，有财此有用。", "The superior man bends his attention to the cultivation of his virtue. When virtue is there, people will come; when people are there, there will be territory; when there is territory, there will be wealth; when there is wealth, there will be the means of use.")
    lu "[line]"
    voice "vo_lu_mat_a2.ogg"
    $ line = t("德者，本也；财者，末也。外本内末，争民施夺。", "Virtue is the root; wealth is the fruit. When the root is neglected and the fruit is sought after, the people will be stirred up to contention and rapine.")
    lu "[line]"
    voice "vo_lu_mat_a3.ogg"
    $ line = t("是故财聚则民散，财散则民聚。是故言悖而出者，亦悖而入；货悖而入者，亦悖而出。", "Hence, when wealth is gathered together, the people are scattered; when wealth is scattered, the people are gathered together. Hence, when words go forth contrary to reason, they will return contrary to reason; when wealth comes in contrary to reason, it will depart contrary to reason.")
    lu "[line]"
    voice "vo_lu_mat_a4.ogg"
    $ line = t("《康诰》曰：「惟命不于常。」道善则得之，不善则失之矣。", "The Announcement to Kang says, The decree is not always the same. Good conduct obtains it; bad conduct loses it.")
    lu "[line]"
    voice "vo_lu_mat_a5.ogg"
    $ line = t("《楚书》曰：「楚国无以为宝，惟善以为宝。」", "The Book of Chu says, 'Chu has no treasure but goodness.'")
    lu "[line]"
    voice "vo_lu_mat_a6.ogg"
    $ line = t("舅犯曰：「亡人无以为宝，仁亲以为宝。」", "Jiu Fan said, 'The fugitive prince has no treasure but his benevolent affection for his relatives.'")
    lu "[line]"

    jump ga_material_choice

label lu_material_b:
    voice "vo_lu_mat_b.ogg"
    $ line = t("王何必曰利？亦有仁义而已矣。", "Why must your Majesty use that word profit? What I have are benevolence and righteousness, and these are my only themes.")
    lu "[line]"

    voice "vo_lu_mat_b2.ogg"
    $ line = t("王曰「何以利吾国」？大夫曰「何以利吾家」？士庶人曰「何以利吾身」？", "If your Majesty says, What will profit my kingdom? the great officers will say, What will profit my family? and the scholars and common people will say, What will profit myself?")
    lu "[line]"
    voice "vo_lu_mat_b3.ogg"
    $ line = t("上下交征利而国危矣。", "Superiors and inferiors will thus strive together after profit, and the kingdom will be endangered.")
    lu "[line]"
    voice "vo_lu_mat_b5.ogg"
    $ line = t("万乘之国弑其君者，必千乘之家；千乘之国弑其君者，必百乘之家。", "For in a kingdom of ten thousand chariots, the murderer of its sovereign will be sure to be the head of a family of a thousand chariots; in a kingdom of a thousand chariots, the murderer of its sovereign will be sure to be the head of a family of a hundred chariots.")
    lu "[line]"
    voice "vo_lu_mat_b6.ogg"
    $ line = t("万取千焉，千取百焉，不为不多矣。", "There are ten thousand in the one, and a thousand in the other—these are not few.")
    lu "[line]"
    voice "vo_lu_mat_b7.ogg"
    $ line = t("苟为后义而先利，不夺不餍。", "But if righteousness be put last, and profit be put first, they will not be satisfied without grasping the whole.")
    lu "[line]"
    voice "vo_lu_mat_b4.ogg"
    $ line = t("未有仁而遗其亲者也，未有义而后其君者也。", "Never has there been benevolence in whose heart the love of his parents was wanting. Never has there been righteousness in whose heart regard to his prince was wanting.")
    lu "[line]"
    jump ga_material_choice

label lu_material_c:
    voice "vo_lu_mat_c.ogg"
    $ line = t("生财有大道：生之者众，食之者寡，为之者疾，用之者舒，则财恒足矣。", "There is a great way for the production of wealth: let the producers be many, and the consumers few; let the workers be active, and the spenders moderate; then wealth will always be sufficient.")
    lu "[line]"

    voice "vo_lu_mat_c2.ogg"
    $ line = t("仁者以财发身，不仁者以身发财。", "The benevolent man makes wealth advance his person; the unbenevolent man makes his person advance wealth.")
    lu "[line]"
    voice "vo_lu_mat_c5.ogg"
    $ line = t("未有上好仁而下不好义者也，未有好义其事不终者也，未有府库财非其财者也。", "Never has there been a prince of superior character, in whose court inferiors were not fond of righteousness. Never has there been a prince fond of righteousness, whose affairs were not brought to a successful issue. Never has there been a state whose treasury was not well filled, while its wealth was righteously administered.")
    lu "[line]"
    voice "vo_lu_mat_c3.ogg"
    $ line = t("孟献子曰：「畜马乘，不察于鸡豚；伐冰之家，不畜牛羊；百乘之家，不畜聚敛之臣。与其有聚敛之臣，宁有盗臣。」", "Meng Xian said, A minister who keeps horses and chariots will not look after poultry and pigs. A family that has stores of ice will not rear oxen and sheep. A family of a hundred chariots will not keep a minister to scrape together wealth. It is better to have a minister who robs the state, than one who scrapes together wealth.")
    lu "[line]"
    voice "vo_lu_mat_c4.ogg"
    $ line = t("此谓国不以利为利，以义为利也。", "This shows that a kingdom should not make profit its aim, but righteousness.")
    lu "[line]"
    jump ga_material_choice

label ga_material_choice:
    scene art14_choice_west with fade
    # 加利利拿撒勒人三选一
    $ opt_a = t("聆听「天上之财宝」", "Hear: Treasures in Heaven")
    $ opt_b = t("聆听「无知财主」", "Hear: The Rich Fool")
    $ opt_c = t("聆听「财主进天国」", "Hear: Camel Through the Needle")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            $ wrong_material += 1
            jump ga_material_a
        "[tag_b]":
            $ wrong_material += 1
            jump ga_material_b
        "[tag_c]":
            jump ga_material_c

label ga_material_a:
    voice "vo_ga_mat_a.ogg"
    $ line = t("不要为自己积攒财宝在地上，地上有虫子咬，能锈坏，也有贼挖窟窿来偷；", "Lay not up for yourselves treasures upon earth, where moth and rust doth corrupt, and where thieves break through and steal:")
    ga "[line]"
    voice "vo_ga_mat_a2.ogg"
    $ line = t("只要积攒财宝在天上，天上没有虫子咬，不能锈坏，也没有贼挖窟窿来偷。", "But lay up for yourselves treasures in heaven, where neither moth nor rust doth corrupt, and where thieves do not break through nor steal:")
    ga "[line]"
    voice "vo_ga_mat_a3.ogg"
    $ line = t("因为你的财宝在哪里，你的心也在哪里。", "For where your treasure is, there will your heart be also.")
    ga "[line]"
    jump youth_material_rebut

label ga_material_b:
    voice "vo_ga_mat_b.ogg"
    $ line = t("有一个财主，田产丰盛，自己心里思想说：「我的出产没有地方收藏，怎么办呢？」", "The ground of a certain rich man brought forth plentifully: And he thought within himself, saying, What shall I do, because I have no room where to bestow my fruits?")
    ga "[line]"
    voice "vo_ga_mat_b2.ogg"
    $ line = t("又说：「我要这么办：要把我的仓房拆了，另盖更大的，在那里收藏我一切的粮食和财物，", "And he said, This will I do: I will pull down my barns, and build greater; and there will I bestow all my fruits and my goods.")
    ga "[line]"
    voice "vo_ga_mat_b3.ogg"
    $ line = t("然后要对我的灵魂说：灵魂哪，你有许多财物积存，可作多年的费用，只管安安逸逸地吃喝快乐吧！」", "And I will say to my soul, Soul, thou hast much goods laid up for many years; take thine ease, eat, drink, and be merry.")
    ga "[line]"
    voice "vo_ga_mat_b4.ogg"
    $ line = t("神却对他说：「无知的人哪，今夜必要你的灵魂，你所预备的要归谁呢？」", "But God said unto him, Thou fool, this night thy soul shall be required of thee: then whose shall those things be, which thou hast provided?")
    ga "[line]"
    voice "vo_ga_mat_b5.ogg"
    $ line = t("凡为自己积财，在神面前不富足的，也是这样。", "So is he that layeth up treasure for himself, and is not rich toward God.")
    ga "[line]"
    jump youth_material_rebut

label ga_material_c:
    voice "vo_ga_mat_c.ogg"
    $ line = t("我实在告诉你们，财主进天国是难的。", "Verily I say unto you, That a rich man shall hardly enter into the kingdom of heaven.")
    ga "[line]"
    voice "vo_ga_mat_c2.ogg"
    $ line = t("我又告诉你们，骆驼穿过针的眼，比财主进神的国还容易呢。", "And again I say unto you, It is easier for a camel to go through the eye of a needle, than for a rich man to enter into the kingdom of God.")
    ga "[line]"
    voice "vo_ga_mat_c4.ogg"
    $ line = t("门徒听见这话，就希奇得很，说：「这样谁能得救呢？」", "When his disciples heard it, they were exceedingly amazed, saying, Who then can be saved?")
    ga "[line]"

    voice "vo_ga_mat_c3.ogg"
    $ line = t("在人这是不能的，在神凡事都能。", "With men this is impossible; but with God all things are possible.")
    ga "[line]"
    jump youth_material_rebut

label youth_material_rebut:
    voice "vo_narr_020.ogg"
    scene art15_wild_laugh with fade
    $ line = t("少年放肆地笑道，眼里闪烁着轻蔑与挑衅。", "The youth laughed wildly, scorn and defiance flashing in his eyes.")
    narrator "[line]"

    voice "vo_s_013.ogg"
    $ line = t("所以说，归根结底，你们不还是不厌其烦地老调重弹着这些陈词滥调吗？", "So after all, you are just harping on the same old tired platitudes, aren't you?")
    s "[line]"

    voice "vo_s_014.ogg"
    $ line = t("表面上满是「君子」与「德」、「蔑财」与「心」，实际上也还是满嘴胡吣！", "All this talk of gentleman and virtue, of despising wealth and the heart—it is all nothing but empty words!")
    s "[line]"

    voice "vo_conf_002.ogg"
    $ line = t("文犹质也，质犹文也。虎豹之鞟犹犬羊之鞟。", "Ornament is as the substance; the substance is as ornament. The skins of a tiger or a leopard stripped of their hair are no different from the skins of a dog or a sheep.")
    conf "[line]"

    voice "vo_monk_002.ogg"
    $ line = t("此乃「加利利的迦拿之酒」。", "This is the wine of Cana in Galilee.")
    monk "[line]"

    voice "vo_s_015.ogg"
    scene art16_standoff with fade
    $ line = t("空口无凭，那你们在这方面的修为又如何？", "Empty words, all of them. What of your own conduct in this regard, then?")
    s "[line]"

    # 孔门儒生三选一
    $ opt_a = t("聆听「陈蔡绝粮」", "Hear: Besieged in Chen and Cai")
    $ opt_b = t("聆听「楚封孔子」", "Hear: King Zhao's Enfeoffment")
    $ opt_c = t("聆听「修己安人」", "Hear: Cultivating Oneself")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump conf_material_a
        "[tag_b]":
            $ wrong_material += 1
            jump conf_material_b
        "[tag_c]":
            $ wrong_material += 1
            jump conf_material_c

label conf_material_a:
    voice "vo_conf_mat_a.ogg"
    $ line = t("孔子迁于蔡三岁，吴伐陈。楚救陈，军于城父。闻孔子在陈蔡之间，楚使人聘孔子。", "Confucius had been in Cai for three years, when Wu invaded Chen. Chu came to the relief of Chen. Hearing that Confucius was between Chen and Cai, the prince of Chu sent messengers to invite him.")

    conf "[line]"
    voice "vo_conf_mat_a6.ogg"
    $ line = t("孔子将往拜礼。", "Confucius was about to go and pay his respects,")
    conf "[line]"
    voice "vo_conf_mat_a7.ogg"
    $ line = t("陈蔡大夫谋曰：「孔子贤者，所刺讥皆中诸侯之疾。今者久留陈蔡之间，诸大夫所设行皆非仲尼之意。」", "when the great officers of Cai and Chen took counsel together, saying, 'Confucius is a man of virtue and ability. What he finds fault with in the princes, hits the sore point of their government. He has been long here between Chen and Cai, and the measures of all the great officers are contrary to his mind.'")
    conf "[line]"

    voice "vo_conf_mat_a2.ogg"
    $ line = t("今楚，大国也，来聘孔子。孔子用于楚，则陈蔡用事大夫危矣。", "Now Chu is a great state, and has sent to invite Confucius. If he should be employed in Chu, then we, the great officers of Chen and Cai, should be in danger.")
    conf "[line]"
    voice "vo_conf_mat_a3.ogg"
    $ line = t("于是乃相与发徒役围孔子于野。不得行，绝粮。从者病，莫能兴。", "Thereupon they jointly sent out their followers to surround Confucius in the wilderness. He could not proceed, and his supplies of food were exhausted. His followers became ill, and were not able to rise.")
    conf "[line]"
    voice "vo_conf_mat_a4.ogg"
    $ line = t("孔子讲诵弦歌不衰。子路愠见曰：「君子亦有穷乎？」", "But Confucius continued to teach, and chant, and string his lute without ceasing. Zi Lu, full of displeasure, came to him and said, Has the superior man indeed to endure such distress?")
    conf "[line]"
    voice "vo_conf_mat_a5.ogg"
    $ line = t("孔子曰：「君子固穷，小人穷斯滥矣。」", "Confucius said, The superior man maintains his firmness in distress; the small man, when in distress, gives way to unbridled license.")
    conf "[line]"
    jump monk_material_choice

label conf_material_b:
    voice "vo_conf_mat_b.ogg"
    $ line = t("楚昭王将以书社地七百里封孔子。楚令尹子西曰：「王之使使诸侯有如子贡者乎？」曰：「无有。」", "King Zhao of Chu was about to give Confucius the territory of seven hundred li. But Zi Xi, the chief minister of Chu, said to him, Has your Majesty any ambassador to the princes like Zi Gong? No, was the reply.")
    conf "[line]"
    voice "vo_conf_mat_b2.ogg"
    $ line = t("「王之辅相有如颜回者乎？」曰：「无有。」「王之将率有如子路者乎？」曰：「无有。」", "Has your Majesty any minister to assist you like Yan Hui? No. Has your Majesty any general like Zi Lu? No.")
    conf "[line]"
    voice "vo_conf_mat_b5.ogg"
    $ line = t("「王之官尹有如宰予者乎？」曰：「无有。」", "Has your Majesty any officer of administration like Zai Yu? No was the reply.")
    conf "[line]"
    voice "vo_conf_mat_b6.ogg"
    $ line = t("「且楚之祖封于周，号为子男五十里。」", "Moreover, the ancestor of Chu received his appointment from Zhou, with the title of baron, and a territory of fifty li square.")
    conf "[line]"

    voice "vo_conf_mat_b3.ogg"
    $ line = t("「今孔丘述三五之法，明周召之业，王若用之，则楚安得世世堂堂方数千里乎？」", "Now Confucius is setting forth the ways of the Three Kings and Five Lords. If your Majesty employ him, how shall Chu go on to possess its territory of thousands of li square, from generation to generation?")
    conf "[line]"
    voice "vo_conf_mat_b4.ogg"
    $ line = t("昭王乃止。", "On this King Zhao desisted.")
    conf "[line]"
    jump monk_material_choice

label conf_material_c:
    voice "vo_conf_mat_c.ogg"
    $ line = t("子路问君子。子曰：「修己以安人。」", "Zi Lu asked what constituted a superior man. The Master said, He cultivates himself so as to be in a state of respectful carefulness.")
    conf "[line]"
    voice "vo_conf_mat_c2.ogg"
    $ line = t("曰：「如斯而已乎？」曰：「修己以安百姓。修己以安百姓，尧舜其犹病诸？」", "And is that all? said Zi Lu. He cultivates himself so as to give rest to all the people. To cultivate himself so as to give rest to all the people—even Yao and Shun would have found this a difficult task.")
    conf "[line]"
    voice "vo_conf_mat_c3.ogg"
    $ line = t("原壤夷俟。子曰：「幼而不孙弟，长而无述焉，老而不死，是为贼。」以杖叩其胫。", "Yuan Rang waited for him in a squatting posture. The Master said to him, In youth, you showed no respect to your elders; in manhood, you have achieved nothing; in old age, you go on living and do not die: you are a thief. And with his staff he tapped his leg.")
    conf "[line]"
    voice "vo_conf_mat_c4.ogg"
    $ line = t("阙党童子将命。或问之曰：「益者与？」子曰：「吾见其居于位也，见其与先生并行也，非求益者也，欲速成者也。」", "A boy of the village of Que was conveying a message. Some one said, 'He will make progress, will he not?' The Master said, 'I see him sitting in his place as if he were a full-grown man; I see him walking along with his seniors as if he were their equal. He is not one seeking progress, he is one who would be quick to be a full-grown man.'")
    conf "[line]"

    jump monk_material_choice

label monk_material_choice:
    # 苦行修士司祭三选一
    $ opt_a = t("聆听「旷野三试」", "Hear: The Three Temptations")
    $ opt_b = t("聆听「勿忧衣食」", "Hear: Take No Thought")
    $ opt_c = t("聆听「勿爱世界」", "Hear: Love Not the World")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            $ wrong_material += 1
            jump monk_material_a
        "[tag_b]":
            jump monk_material_b
        "[tag_c]":
            $ wrong_material += 1
            jump monk_material_c

label monk_material_a:
    voice "vo_monk_mat_a.ogg"
    $ line = t("当时，耶稣被圣灵引到旷野，受魔鬼的试探。他禁食四十昼夜，后来就饿了。", "Then was Jesus led up of the Spirit into the wilderness to be tempted of the devil. And when he had fasted forty days and forty nights, he was afterward an hungred.")
    monk "[line]"
    voice "vo_monk_mat_a2.ogg"
    $ line = t("那试探人的进前来，对他说：「你若是神的儿子，可以吩咐这些石头变成食物。」", "And when the tempter came to him, he said, If thou be the Son of God, command that these stones be made bread.")
    monk "[line]"
    voice "vo_monk_mat_a3.ogg"
    $ line = t("耶稣却回答说：「经上记着说：『人活着，不是单靠食物，乃是靠神口里所出的一切话。』」", "But he answered and said, It is written, Man shall not live by bread alone, but by every word that proceedeth out of the mouth of God.")
    monk "[line]"
    voice "vo_monk_mat_a4.ogg"
    $ line = t("魔鬼又带他上了一座最高的山，将世上的万国与万国的荣华都指给他看，", "Again, the devil taketh him up into an exceeding high mountain, and sheweth him all the kingdoms of the world, and the glory of them;")
    monk "[line]"
    voice "vo_monk_mat_a5.ogg"
    $ line = t("对他说：「你若俯伏拜我，我就把这一切都赐给你。」", "And saith unto him, All these things will I give thee, if thou wilt fall down and worship me.")
    monk "[line]"
    voice "vo_monk_mat_a6.ogg"
    $ line = t("耶稣说：「撒但，退去吧！因为经上记着说：『当拜主你的神，单要事奉他。』」", "Then saith Jesus unto him, Get thee hence, Satan: for it is written, Thou shalt worship the Lord thy God, and him only shalt thou serve.")
    monk "[line]"
    voice "vo_monk_mat_a7.ogg"
    $ line = t("于是魔鬼离了耶稣，有天使来伺候他。", "Then the devil leaveth him, and, behold, angels came and ministered unto him.")
    monk "[line]"
    jump material_end

label monk_material_b:
    voice "vo_monk_mat_b.ogg"
    $ line = t("所以我告诉你们：不要为生命忧虑吃什么，喝什么；为身体忧虑穿什么。", "Therefore I say unto you, Take no thought for your life, what ye shall eat, or what ye shall drink; nor yet for your body, what ye shall put on.")
    monk "[line]"
    voice "vo_monk_mat_b2.ogg"
    $ line = t("生命不胜于饮食吗？身体不胜于衣裳吗？", "Is not the life more than meat, and the body than raiment?")
    monk "[line]"
    voice "vo_monk_mat_b3.ogg"
    $ line = t("你们看天上的飞鸟，也不种，也不收，也不积蓄在仓里，你们的天父尚且养活它。你们不比飞鸟贵重得多吗？", "Behold the fowls of the air: for they sow not, neither do they reap, nor gather into barns; yet your heavenly Father feedeth them. Are ye not much better than they?")
    monk "[line]"
    voice "vo_monk_mat_b4.ogg"
    $ line = t("你们哪一个能用思虑使寿数多加一刻呢？", "Which of you by taking thought can add one cubit unto his stature?")
    monk "[line]"
    jump material_end

label monk_material_c:
    voice "vo_monk_mat_c.ogg"
    $ line = t("不要爱世界和世界上的事。人若爱世界，爱父的心就不在他里面了。", "Love not the world, neither the things that are in the world. If any man love the world, the love of the Father is not in him.")
    monk "[line]"
    voice "vo_monk_mat_c2.ogg"
    $ line = t("因为凡世界上的事，就像肉体的情欲，眼目的情欲，并今生的骄傲，都不是从父来的，乃是从世界来的。", "For all that is in the world, the lust of the flesh, and the lust of the eyes, and the pride of life, is not of the Father, but is of the world.")
    monk "[line]"
    voice "vo_monk_mat_c3.ogg"
    $ line = t("这世界和其上的情欲都要过去，惟独遵行神旨意的，是永远常存。", "And the world passeth away, and the lust thereof: but he that doeth the will of God abideth for ever.")
    monk "[line]"
    jump material_end

label material_end:
    # 第一审结算：四组三选一，错到一半就判 ♦
    if wrong_material >= 2:
        $ win_material = 0
        jump material_bad
    $ win_material = 1

    voice "vo_narr_021.ogg"
    scene art17_realize with fade
    $ line = t("少年沉思了一阵，他觉得自己理解得过于肤浅，而当他领悟到其中蕴意后，赧颜汗下。", "The youth fell silent, pondering. He had thought his own understanding shallow, but as the meaning of the words dawned on him, a flush of shame burned across his face.")
    narrator "[line]"

    voice "vo_narr_022.ogg"
    $ line = t("以前，他总觉得他对物质生活孜孜以求，精神上的富足便会悄然而至。", "Once he had thought that if he strove ceaselessly for material comfort, spiritual fulfillment would follow of its own accord.")
    narrator "[line]"

    voice "vo_narr_023.ogg"
    $ line = t("直到他面对现实时，自己对物质利益锱铢必较，对优越的住房、富足的餐饮、成功的事业也如他人般趋之若鹜。", "But when he faced the truth, he saw how he had haggled over every trivial gain, how he had coveted fine houses, rich food, and worldly success just like everyone else.")
    narrator "[line]"

    voice "vo_narr_024.ogg"
    $ line = t("他也曾幻想着独属自己的罗特希尔德思想，可到头来却总感到一种心灵上的寂寥与空荡，感到自己迷失了什么……", "He had once dreamed of a Rothschild-like fortune of his own, yet in the end he always felt a hollow emptiness in his soul, as if something were lost…")
    narrator "[line]"

    voice "vo_narr_025.ogg"
    $ line = t("但他确信，不论明里暗里，眼下伫立在他身前的两位圣人定不单单在宣扬自己的教义，此中当还有别的深意……", "Yet he knew, in his heart of hearts, that the two sages standing before him were not merely preaching their doctrines—there was a deeper meaning beneath it all.")
    narrator "[line]"

    jump material_done

label material_bad:
    # —— 第一审 ♦：少年没被说服 ——
    voice "vo_narr_059.ogg"
    $ line = t("少年思索了一会儿，觉得自己在现实中有时确也对物质生活的丰糜过度执迷，成为某些人口中精致的利己主义者。", "The youth pondered for a while. He admitted that in real life he did at times grow overly obsessed with material abundance, becoming what some called a refined egoist.")
    narrator "[line]"

    voice "vo_narr_060.ogg"
    $ line = t("但纵使他面前的两位尊者的言语义有所取，还是难以让他信服：", "Still, even granting that there was merit in the words of the two revered figures before him, he remained unconvinced.")
    narrator "[line]"

    voice "vo_narr_061.ogg"
    $ line = t("倘若这种谴责是针对社会的与群像的，那我无意置辩，尽管这听起来更像是浪漫主义的尘言旧论；", "If such condemnation was directed at society and the masses, he would raise no objection, though it sounded like old romantic rhetoric.")
    narrator "[line]"

    voice "vo_narr_062.ogg"
    $ line = t("但如果仅是针对我个人的话，那我自当直辞雪谤。更何况无物质充作基底，又怎能强求精神神完意裕呢……", "Yet if it was aimed solely at him as an individual, he must speak out to clear his name. Moreover: without material substance as a foundation, how could one possibly demand full-bodied spiritual wholeness?")
    narrator "[line]"

    voice "vo_narr_063.ogg"
    $ line = t("少年不解此审。", "The youth could not comprehend this trial.")
    narrator "[line]"

    jump material_done

label material_done:
    scene art18_gloomy with fade
    # ========== 第二审：虚无 ==========
    voice "vo_narr_026.ogg"
    $ line = t("—— 第二审：虚无 ——", "—— Second Trial: Emptiness ——")
    narrator "[line]"

    voice "vo_narr_027.ogg"
    $ line = t("少年收敛了些许矜持感，但还是保持着某种悒郁不平的态度。", "The youth had toned down some of his haughty defiance, yet there was still a sullen, resentful edge to his voice.")
    narrator "[line]"

    voice "vo_s_016.ogg"
    $ line = t("你们说我虚无、随波逐流、不冷不热？", "You call me empty, adrift, neither cold nor hot?")
    s "[line]"

    voice "vo_s_017.ogg"
    $ line = t("难道就因为我对住房之优越、食粮之丰盈、就业之上进等等黾勉求之就可断言我虚无吗？", "Is it simply because I strive for a good house, plenty of food, and advancement in my work that you condemn me as empty?")
    s "[line]"

    voice "vo_s_018.ogg"
    $ line = t("我对生活有方向感与目标，那又何谈虚无？", "I have direction and goals in my life. How can you call that emptiness?")
    s "[line]"

    voice "vo_s_019.ogg"
    $ line = t("就算你们为此说我物质，但你们也不能否认我为此而在精神上虚无！", "Even if you blame me for being materialistic, you cannot deny that my pursuit of these things leaves me spiritually empty!")
    s "[line]"

    voice "vo_s_020.ogg"
    $ line = t("鲁鄹邑来的，我知道你是想借此说我违逆你君子之道，违逆你仁义之德；", "You of Zou, I know you mean to say I transgress your way of the gentleman, your virtue of benevolence.")
    s "[line]"

    voice "vo_s_021.ogg"
    $ line = t("还有那远在加利利的，我也知道你是想说我因未担我们那听了蛇的挑唆，食了禁果而后能辩孰善孰恶的先祖的原罪。", "And you of far-off Galilee, I know you mean to speak of original sin—of our ancestors who listened to the serpent's temptation, ate the forbidden fruit, and came to know good and evil.")
    s "[line]"

    voice "vo_s_022.ogg"
    $ line = t("但你们错了，我并非没有自己的信仰，相反，我一生对我那理想的美好的生活的信念孜孜以求，矢志不渝！", "But you are wrong. It is not that I have no faith. On the contrary, I have striven all my life with unswerving devotion toward my ideal of a good life.")
    s "[line]"

    scene art19_choice3 with fade
    # 鲁鄹邑人三选一
    $ opt_a = t("聆听「乡愿之辩」", "Hear: On the Village Worthies")
    $ opt_b = t("聆听「和而不同」", "Hear: Harmony Without Uniformity")
    $ opt_c = t("聆听「弘毅守道」", "Hear: The Scholar's Vast Resolve")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            $ wrong_emptiness += 1
            jump lu_emptiness_a
        "[tag_b]":
            jump lu_emptiness_b
        "[tag_c]":
            $ wrong_emptiness += 1
            jump lu_emptiness_c

label lu_emptiness_a:
    voice "vo_lu_emp_a.ogg"
    $ line = t("不得中道而与之，必也狂狷乎！狂者进取，狷者有所不为也。", "Men who hold fast the middle course, but will not in all things come up to it, must at least be of two classes—the enterprising and the strictly reserved.")
    lu "[line]"
    voice "vo_lu_emp_a2.ogg"
    $ line = t("过我门而不入我室，我不憾焉者，其惟乡原乎！乡原，德之贼也。", "But there are those who pass my door and do not enter my house, and whom I do not regret not having. They are the village worthies! The village worthies are the thieves of virtue.")
    lu "[line]"
    voice "vo_lu_emp_a3.ogg"
    $ line = t("恶似而非者：恶莠，恐其乱苗也；恶佞，恐其乱义也；恶利口，恐其乱信也；", "There are things which seem right, but are not right. There are weeds which resemble grain, and are feared for confounding the grain.")
    lu "[line]"
    voice "vo_lu_emp_a4.ogg"
    $ line = t("恶郑声，恐其乱乐也；恶紫，恐其乱朱也；恶乡原，恐其乱德也。", "There are the songs of Zheng which are feared for confounding the graver music. There are the purple which are feared for confounding the true red. There are the village worthies who are feared for confounding virtue.")
    lu "[line]"
    jump ga_emptiness_choice

label lu_emptiness_b:
    voice "vo_lu_emp_b.ogg"
    $ line = t("君子和而不同，小人同而不和。", "The superior man is affable, but not adulatory; the mean man is adulatory, but not affable.")
    lu "[line]"
    voice "vo_lu_emp_b2.ogg"
    $ line = t("子贡问曰：「乡人皆好之，何如？」子曰：「未可也。」", "Zi Gong asked, saying, What do you think of a man who is loved by all his fellow-villagers? The Master said, I will not tell you that.")
    lu "[line]"
    voice "vo_lu_emp_b3.ogg"
    $ line = t("「乡人皆恶之，何如？」子曰：「未可也。不如乡人之善者好之，其不善者恶之。」", "And what do you think of one who is hated by all his fellow-villagers? The Master said, I will not tell you that. It is not so good as that the good men of the village love him, and the bad men hate him.")
    lu "[line]"
    voice "vo_lu_emp_b4.ogg"
    $ line = t("叶公语孔子曰：「吾党有直躬者，其父攘羊，而子证之。」", "The Duke of She addressed Confucius, saying, Among us, there is a man called Upright Gong. His father stole a sheep, and he bore witness against him.")
    lu "[line]"
    voice "vo_lu_emp_b5.ogg"
    $ line = t("孔子曰：「吾党之直者异于是：父为子隐，子为父隐，直在其中矣。」", "Confucius said, The upright men among us are different from this. The father conceals the fault of the son, and the son conceals the fault of the father. Uprightness is to be found in this.")
    lu "[line]"
    jump ga_emptiness_choice

label lu_emptiness_c:
    voice "vo_lu_emp_c.ogg"
    $ line = t("士不可以不弘毅，任重而道远。仁以为己任，不亦重乎？死而后已，不亦远乎？", "The scholar may not be without breadth of mind and vigorous endurance. His burden is heavy and his course is long. Virtue is the burden which he deems it his duty to bear; is it not heavy? It is only with death that his course ends; is it not long?")
    lu "[line]"
    voice "vo_lu_emp_c2.ogg"
    $ line = t("笃信好学，守死善道。危邦不入，乱邦不居。", "Sincerely to believe in learning, and firmly to maintain the good way. Enter not a state which is in peril, nor dwell in one which is in rebellion.")
    lu "[line]"
    voice "vo_lu_emp_c3.ogg"
    $ line = t("天下有道则见，无道则隐。邦有道，贫且贱焉，耻也；邦无道，富且贵焉，耻也。", "When the world is right, let him show himself; when it is wrong, let him keep retired. When good government prevails in a state, to be poor and in a low condition is a thing to be ashamed of. When bad government prevails, to be rich and in honor is a thing to be ashamed of.")
    lu "[line]"
    jump ga_emptiness_choice

label ga_emptiness_choice:
    scene art20_choice4 with fade
    $ opt_a = t("聆听「温水灵魂」", "Hear: The Lukewarm Soul")
    $ opt_b = t("聆听「初心弃离」", "Hear: Left Thy First Love")
    $ opt_c = t("聆听「莫自欺」", "Hear: Be Not Deceived")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump ga_emptiness_a
        "[tag_b]":
            $ wrong_emptiness += 1
            jump ga_emptiness_b
        "[tag_c]":
            $ wrong_emptiness += 1
            jump ga_emptiness_c

label ga_emptiness_a:
    voice "vo_ga_emp_a0.ogg"
    $ line = t("你要写信给老底嘉教会的使者，说：那为阿们的，为诚信真实见证的，在神创造万物之上为元首的，说：", "And unto the angel of the church of the Laodiceans write: These things saith the Amen, the faithful and true witness, the beginning of the creation of God:")
    ga "[line]"

    voice "vo_ga_emp_a.ogg"
    $ line = t("我知道你的行为，你也不冷也不热；我巴不得你或冷或热。", "I know thy works, that thou art neither cold nor hot: I would thou wert cold or hot.")
    ga "[line]"
    voice "vo_ga_emp_a2.ogg"
    $ line = t("你既如温水，也不冷也不热，所以我必从我口中把你吐出去。", "So then because thou art lukewarm, and neither cold nor hot, I will spue thee out of my mouth.")
    ga "[line]"
    voice "vo_ga_emp_a3.ogg"
    $ line = t("你说：我是富足，已经发了财，一样都不缺；却不知道你是那困苦、可怜、贫穷、瞎眼、赤身的。", "Because thou sayest, I am rich, and increased with goods, and have need of nothing; and knowest not that thou art wretched, and miserable, and poor, and blind, and naked:")
    ga "[line]"
    jump youth_emptiness_q

label ga_emptiness_b:
    voice "vo_ga_emp_b.ogg"
    $ line = t("然而有一件事我要责备你，就是你把起初的爱心离弃了。", "Nevertheless I have somewhat against thee, because thou hast left thy first love.")
    ga "[line]"
    voice "vo_ga_emp_b2.ogg"
    $ line = t("所以应当回想你是从哪里坠落的，并要悔改，行起初所行的事。", "Remember therefore from whence thou art fallen, and repent, and do the first works;")
    ga "[line]"
    voice "vo_ga_emp_b3.ogg"
    $ line = t("你若不悔改，我就临到你那里，把你的灯台从原处挪去。", "or else I will come unto thee quickly, and will remove thy candlestick out of his place, except thou repent.")
    ga "[line]"
    jump youth_emptiness_q

label ga_emptiness_c:
    voice "vo_ga_emp_c.ogg"
    $ line = t("人若无有，自己还以为有，就是自欺了。", "For if a man think himself to be something, when he is nothing, he deceiveth himself.")
    ga "[line]"
    voice "vo_ga_emp_c2.ogg"
    $ line = t("各人应当察验自己的行为，这样，他所夸的就专在自己，不在别人了。", "But let every man prove his own work, and then shall he have rejoicing in himself alone, and not in another.")
    ga "[line]"
    voice "vo_ga_emp_c4.ogg"
    $ line = t("因为各人必担当自己的担子。我们在道理上受教的，就当将一切善事供给教法师。", "For every man shall bear his own burden. Let him that is taught in the word communicate unto him that teacheth in all good things.")
    ga "[line]"

    voice "vo_ga_emp_c3.ogg"
    $ line = t("不要自欺，神是轻慢不得的。人种的是什么，收的也是什么。", "Be not deceived; God is not mocked: for whatsoever a man soweth, that shall he also reap.")
    ga "[line]"
    jump youth_emptiness_q

label youth_emptiness_q:
    scene art21_struggle with fade
    voice "vo_narr_028.ogg"
    $ line = t("少年言语里闪烁着困惑与一丝绝望。", "The youth's voice wavered, mingled with confusion and a flicker of despair.")
    narrator "[line]"

    scene art29_choice7 with fade
    # 孔门儒生三选一
    $ opt_a = t("聆听「大丈夫」", "Hear: The Great Man")
    $ opt_b = t("聆听「君子存心」", "Hear: Keeps His Heart")
    $ opt_c = t("聆听「义利分野」", "Hear: Virtue and Profit")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            $ wrong_emptiness += 1
            jump conf_emptiness_a
        "[tag_b]":
            $ wrong_emptiness += 1
            jump conf_emptiness_b
        "[tag_c]":
            jump conf_emptiness_c

label conf_emptiness_a:
    voice "vo_conf_emp_a.ogg"
    $ line = t("居天下之广居，立天下之正位，行天下之大道；", "He dwells in the wide dwelling-place of the world; he stands in the correct position of the world; he walks in the great path of the world.")
    conf "[line]"
    voice "vo_conf_emp_a2.ogg"
    $ line = t("得志，与民由之；不得志，独行其道。", "When he attains his purpose, he shares it with the people; when he fails of his purpose, he pursues his course alone.")
    conf "[line]"
    voice "vo_conf_emp_a3.ogg"
    $ line = t("富贵不能淫，贫贱不能移，威武不能屈，此之谓大丈夫。", "Riches and honors cannot corrupt him; poverty and mean condition cannot make him swerve; power and authority cannot subdue him. Such a man is called a great man.")
    conf "[line]"
    jump monk_emptiness_choice

label conf_emptiness_b:
    voice "vo_conf_emp_b.ogg"
    $ line = t("君子所以异于人者，以其存心也。君子以仁存心，以礼存心。", "That whereby the superior man is distinguished from other men is this: he keeps his heart in benevolence and in propriety.")
    conf "[line]"
    voice "vo_conf_emp_b2.ogg"
    $ line = t("仁者爱人，有礼者敬人。爱人者，人恒爱之；敬人者，人恒敬之。", "The benevolent man loves others; the man of propriety respects others. He who loves others is constantly loved by them; he who respects others is constantly respected by them.")
    conf "[line]"
    voice "vo_conf_emp_b3.ogg"
    $ line = t("有人于此，其待我以横逆，则君子必自反也：我必不仁也，必无礼也，此物奚宜至哉？", "Suppose there is a man who treats me with outrageous rudeness. The superior man will then turn round upon himself, and say, I must have been wanting in benevolence, I must have been wanting in propriety—how should this thing have happened to me?")
    conf "[line]"
    jump monk_emptiness_choice

label conf_emptiness_c:
    voice "vo_conf_emp_c.ogg"
    $ line = t("君子怀德，小人怀土；君子怀刑，小人怀惠。", "The superior man thinks of virtue; the small man thinks of comfort. The superior man thinks of the sanctions of law; the small man thinks of favors which he may receive.")
    conf "[line]"
    voice "vo_conf_emp_c2.ogg"
    $ line = t("放于利而行，多怨。君子喻于义，小人喻于利。", "He who sets his mind on gain will do much that is to be murmured at. The superior man understands what is right; the small man understands what is profitable.")
    conf "[line]"
    jump monk_emptiness_choice

label monk_emptiness_choice:
    $ opt_a = t("聆听「磐石之屋」", "Hear: House Upon a Rock")
    $ opt_b = t("聆听「德行劝勉」", "Hear: Exhortations to Virtue")
    $ opt_c = t("聆听「听道行道」", "Hear: Be Doers of the Word")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            $ wrong_emptiness += 1
            jump monk_emptiness_a
        "[tag_b]":
            jump monk_emptiness_b
        "[tag_c]":
            $ wrong_emptiness += 1
            jump monk_emptiness_c

label monk_emptiness_a:
    voice "vo_monk_emp_a.ogg"
    $ line = t("凡听见我这话就去行的，好比一个聪明人，把房子盖在磐石上。", "Therefore whosoever heareth these sayings of mine, and doeth them, I will liken him unto a wise man, which built his house upon a rock:")
    monk "[line]"
    voice "vo_monk_emp_a2.ogg"
    $ line = t("雨淋，水冲，风吹，撞着那房子，房子总不倒塌，因为根基立在磐石上。", "And the rain descended, and the floods came, and the winds blew, and beat upon that house; and it fell not: for it was founded upon a rock.")
    monk "[line]"
    voice "vo_monk_emp_a3.ogg"
    $ line = t("凡听见我这话不去行的，好比一个无知的人，把房子盖在沙土上。", "And every one that heareth these sayings of mine, and doeth them not, shall be likened unto a foolish man, which built his house upon the sand:")
    monk "[line]"
    voice "vo_monk_emp_a4.ogg"
    $ line = t("雨淋，水冲，风吹，撞着那房子，房子就倒塌了，并且倒塌得很大。", "And the rain descended, and the floods came, and the winds blew, and beat upon that house; and it fell: and great was the fall of it.")
    monk "[line]"
    jump emptiness_end

label monk_emptiness_b:
    voice "vo_monk_emp_b.ogg"
    $ line = t("爱人不可虚假。恶要厌恶，善要亲近。", "Let love be without dissimulation. Abhor that which is evil; cleave to that which is good.")
    monk "[line]"
    voice "vo_monk_emp_b2.ogg"
    $ line = t("爱弟兄，要彼此亲热；恭敬人，要彼此推让。殷勤，不可懒惰；心里火热，常常服侍主。", "Be kindly affectioned one to another with brotherly love; in honour preferring one another; Not slothful in business; fervent in spirit; serving the Lord;")
    monk "[line]"
    voice "vo_monk_emp_b3.ogg"
    $ line = t("在指望中要喜乐，在患难中要忍耐，祷告要恒切。", "Rejoicing in hope; patient in tribulation; continuing instant in prayer;")
    monk "[line]"
    jump emptiness_end

label monk_emptiness_c:
    voice "vo_monk_emp_c.ogg"
    $ line = t("只是你们要行道，不要单单听道，自己欺哄自己。", "But be ye doers of the word, and not hearers only, deceiving your own selves.")
    monk "[line]"
    voice "vo_monk_emp_c2.ogg"
    $ line = t("因为听道而不行道的，就像人对着镜子看自己本来的面目，看见，走后，随即忘了他的相貌如何。", "For if any be a hearer of the word, and not a doer, he is like unto a man beholding his natural face in a glass: For he beholdeth himself, and goeth his way, and straightway forgetteth what manner of man he was.")
    monk "[line]"
    voice "vo_monk_emp_c3.ogg"
    $ line = t("惟有详细察看那全备、使人自由之律法的，并且时常如此，这人既不是听了就忘，乃是实在行出来，就在他所行的事上必然得福。", "But whoso looketh into the perfect law of liberty, and continueth therein, he being not a forgetful hearer, but a doer of the work, this man shall be blessed in his deed.")
    monk "[line]"
    jump emptiness_end

label emptiness_end:
    # 第二审结算：四组三选一，错到一半就判 ♦
    if wrong_emptiness >= 2:
        $ win_emptiness = 0
        jump emptiness_bad
    $ win_emptiness = 1

    # —— 第二审 ♠：少年被问住了 ——
    scene art21_struggle with fade
    voice "vo_s_023.ogg"
    $ line = t("那我该如何？怎样才能摆脱虚无？", "Then what am I to do? How can I break free from this emptiness?")
    s "[line]"

    voice "vo_narr_029.ogg"
    $ line = t("少年回想起自己对物质的「非虚无」的追求，想起曾为之自诩为「罗特希尔德思想」的一切，以及敛财时那盈溢着贪婪的目光善恶不分的冲动。", "He thought back to his pursuit of material things, which he had insisted were not empty. He thought of all he had called his Rothschild ideal, of the greedy, unprincipled gleam in his eyes as he amassed wealth.")
    narrator "[line]"

    voice "vo_narr_030.ogg"
    $ line = t("其实他心里也清楚，他追求的「一切为经济原则」终究将幻化为泡沫的残影。", "Deep down he knew that the principle of economy he chased would in the end dissolve like a foam shadow.")
    narrator "[line]"

    voice "vo_narr_031.ogg"
    $ line = t("他知道这些所追求的一切终有一天会遇到瓶颈，达到阈值，他也害怕他孜孜以求的同时也是他人所趋之若鹜的一切终被阻滞。", "He knew all his striving would one day hit a ceiling, reach a threshold. He feared that all he pursued, what everyone else pursued, would one day come to a halt.")
    narrator "[line]"

    voice "vo_narr_032.ogg"
    $ line = t("「要是有天我达到了我所追求的一切的终点，我的归宿又何在？」他常常迫使自己思考这个问题。", "\"If one day I reach the end of everything I strive for, where will I be then?\" he had often forced himself to ask.")
    narrator "[line]"

    voice "vo_narr_033.ogg"
    $ line = t("而为了免于此，他有时也会不明里就的霍霍一切，千金散尽，寄希望以此以持续催生自己生活的动力。", "And to escape that question, he would sometimes recklessly spend everything he had, hoping to keep the momentum of his life going.")
    narrator "[line]"

    voice "vo_narr_034.ogg"
    $ line = t("而现在他才真正感到，这一切只是纸糊的一场喜剧，虚无且无义……他懊丧得望着他们，冀望他们能再说些什么……", "But now he truly felt it all was nothing but a paper farce—empty, meaningless… He looked up at them in dejection, longing for them to say more.")
    narrator "[line]"

    scene art22_look_at_them with fade
    # 过渡到第三审
    voice "vo_narr_035.ogg"
    $ line = t("—— 第三审：脱离根基 ——", "—— Third Trial: Severed from the Root ——")
    narrator "[line]"

    scene art23_despair with fade
    voice "vo_narr_036.ogg"
    $ line = t("至此，少年失去了他初来乍到时的那种故作矜持与傲慢的神态，", "By now the youth had shed all the feigned poise and arrogance he had worn when he first entered.")
    narrator "[line]"

    voice "vo_narr_037.ogg"
    $ line = t("他感到一种前所未有的丧落与绝望，对最后的一审也已万念俱灰……", "He felt an unprecedented dejection and despair, and all will to fight the final trial had drained away.")
    narrator "[line]"

    jump emptiness_done

label emptiness_bad:
    # —— 第二审 ♦：少年没被说服 ——
    scene art21_struggle with fade
    voice "vo_s_040.ogg"
    $ line = t("难道真被你们说中？难道我真虚无？倘若如此，那你们又要我如何？", "Can it be that you have truly seen through me? Am I really empty? And if so, what would you have me do?")
    s "[line]"

    voice "vo_narr_064.ogg"
    $ line = t("少年回忆起自己对物质的「非虚无」的追求，以及曾为之自诩为「罗特希尔德思想」的一切，以及敛财时那盈溢着贪婪的目光和善恶不分的冲动……", "The youth recalled his so-called non-empty pursuit of material goods, that which he had named his Rothschild philosophy, together with the greedy, morally blind impulses that stirred within him while accumulating wealth…")
    narrator "[line]"

    voice "vo_narr_065.ogg"
    $ line = t("但他并不认为这就可以被人名之为虚无，且因此而遭人詈骂，因为自己毕竟还是有生活的目标的：", "Yet he refused to accept that this made him hollow and worthy of reproach. After all, he possessed life-goals of his own:")
    narrator "[line]"

    voice "vo_narr_066.ogg"
    $ line = t("有了物质目标的达成，精神丰盈自会接踵而至；而当自身的精神层次达到某一层级，自己自会兼济天下……", "Once material aims were fulfilled, spiritual richness would surely follow. And once his spiritual stature rose to a certain height, he would naturally extend care to the whole world…")
    narrator "[line]"

    voice "vo_narr_067.ogg"
    $ line = t("如此庸庸碌碌便是一大半生，而这一大半生却又是如此充实，怎可埋怨我虚无呢？他倨傲地望着他们，想看看他们会如何回应。", "To toil away like this for most of a lifetime was, to his mind, a life of substance. How could anyone accuse him of emptiness? He gazed haughtily at them, waiting for their reply.")
    narrator "[line]"

    scene art22_look_at_them with fade
    # 过渡到第三审
    voice "vo_narr_035.ogg"
    $ line = t("—— 第三审：脱离根基 ——", "—— Third Trial: Severed from the Root ——")
    narrator "[line]"

    scene art23_despair with fade
    voice "vo_narr_068.ogg"
    $ line = t("至此，少年依旧稀里糊涂，即便自己多少也听进了些许话语，或许也理解了其中的某种蕴意，但他觉得这只不过是局外者对自己的苛刻和怜悯。", "By this point the youth remained confused. Though some words had sunk in and he grasped fragments of their meaning, he believed it was nothing more than outsiders judging him with harshness and pity.")
    narrator "[line]"

    voice "vo_narr_069.ogg"
    $ line = t("「他们从未了解过我，他们也从未设身处地地代入我的处境。」少年如是想。他越来越感到恼怒与焦躁，巴不得快点结束这一切。", "\"They have never truly known me. They have never stood in my shoes,\" he thought. Anger and restlessness welled inside him; he longed for all of this to be over quickly.")
    narrator "[line]"

    jump emptiness_done

label emptiness_done:
    voice "vo_s_024.ogg"
    $ line = t("何为根基？", "What is the root?")
    s "[line]"

    voice "vo_conf_003.ogg"
    $ line = t("我们的人民与传统。", "Our people, and our tradition.")
    conf "[line]"

    scene art24_choice5 with fade
    # 鲁鄹邑人三选一
    $ opt_a = t("聆听「失民则亡」", "Hear: Losing the People Means Ruin")
    $ opt_b = t("聆听「民贵君轻」", "Hear: The People Are Most Important")
    $ opt_c = t("聆听「推恩保民」", "Hear: Extend Kindness to All")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            $ wrong_root += 1
            jump lu_root_a
        "[tag_b]":
            $ wrong_root += 1
            jump lu_root_b
        "[tag_c]":
            jump lu_root_c

label lu_root_a:
    voice "vo_lu_root_a.ogg"
    $ line = t("桀纣之失天下也，失其民也；失其民者，失其心也。", "Jie and Zhou lost the empire because they lost the people. They lost the people because they lost their hearts.")
    lu "[line]"
    voice "vo_lu_root_a2.ogg"
    $ line = t("得天下有道：得其民，斯得天下矣；得其民有道：得其心，斯得民矣；", "There is a way to get the empire: get the people, and you get the empire. There is a way to get the people: win their hearts, and you get the people.")
    lu "[line]"
    voice "vo_lu_root_a3.ogg"
    $ line = t("得其心有道：所欲与之聚之，所恶勿施尔也。", "There is a way to win their hearts: gather for them what they like, and do not lay on them what they dislike.")
    lu "[line]"
    voice "vo_lu_root_a4.ogg"
    $ line = t("民之归仁也，犹水之就下，兽之走圹也。故为渊驱鱼者，獭也；为丛驱爵者，鹯也；", "The people turn to benevolence as naturally as water flows downward, or beasts run to the wilderness. Therefore it is the otter that drives the fish to the deep pool; it is the hawk that drives the sparrows to the thicket;")
    lu "[line]"
    voice "vo_lu_root_a6.ogg"
    $ line = t("为汤武驱民者，桀与纣也。", "it is Jie and Zhou that drive the people to Tang and Wu.")
    lu "[line]"

    voice "vo_lu_root_a5.ogg"
    $ line = t("今天下之君有好仁者，则诸侯皆为之驱矣。虽欲无王，不可得已。", "If there were any prince in the world now who loved benevolence, all the other princes would drive their people to him. Even if he did not wish to become sovereign, he could not avoid it.")
    lu "[line]"
    voice "vo_lu_root_a7.ogg"
    $ line = t("今之欲王者，犹七年之病求三年之艾也。苟为不畜，终身不得。苟不志于仁，终身忧辱，以陷于死亡。", "But those who now desire to be sovereign are like men seeking a three-year-old herb for a seven-year sickness. If it be not stored up now, it will not be got for the whole life. If a man do not set his heart on benevolence, he will be all his life in sorrow and disgrace, and will sink into ruin and death.")
    lu "[line]"
    voice "vo_lu_root_a8.ogg"
    $ line = t("《诗》云：「其何能淑，载胥及溺。」此之谓也。", "It is said in the Book of Poetry, 'How can they be made good? They all sink and drown.' This is the meaning.")
    lu "[line]"

    jump ga_root_choice

label lu_root_b:
    voice "vo_lu_root_b.ogg"
    $ line = t("民为贵，社稷次之，君为轻。", "The people are the most important element in a nation; the spirits of the land and grain are the next; the sovereign is the lightest.")
    lu "[line]"
    voice "vo_lu_root_b2.ogg"
    $ line = t("是故得乎丘民而为天子，得乎天子为诸侯，得乎诸侯为大夫。", "Therefore he who gains the affections of the people becomes sovereign; he who gains the confidence of the sovereign becomes a prince; he who gains the confidence of the prince becomes a great officer.")
    lu "[line]"
    voice "vo_lu_root_b3.ogg"
    $ line = t("诸侯危社稷，则变置。牺牲既成，粢盛既洁，祭祀以时，然而旱干水溢，则变置社稷。", "If the princes endanger the spirits of the land and grain, they are changed for others. When the victims of sacrifice are perfect, and the vessels of grain are clean, and the sacrifices are offered at their proper seasons, yet there are droughts and floods, then the spirits of the land and grain are changed for others.")
    lu "[line]"
    jump ga_root_choice

label lu_root_c:
    voice "vo_lu_root_c.ogg"
    $ line = t("老吾老，以及人之老；幼吾幼，以及人之幼。天下可运于掌。", "Treat the aged of your own family as aged should be treated, and then extend the same treatment to the aged of other families. Treat the young of your own family as young should be treated, and then extend the same treatment to the young of other families. You may govern the whole kingdom as if you were turning it about in your palm.")
    lu "[line]"
    voice "vo_lu_root_c4.ogg"
    $ line = t("《诗》云：「刑于寡妻，至于兄弟，以御于家邦。」言举斯心加诸彼而已。", "It is said in the Book of Poetry, 'His example was an influence on his wife, it extended to his brothers, and so he regulated the family and the state.' The meaning is, that you have just to take this one heart and apply it to that other case.")
    lu "[line]"

    voice "vo_lu_root_c2.ogg"
    $ line = t("故推恩足以保四海，不推恩无以保妻子。", "Therefore the extension of kindness is sufficient to protect all within the four seas; the want of it is sufficient not to protect one's wife and children.")
    lu "[line]"
    voice "vo_lu_root_c3.ogg"
    $ line = t("古之人所以大过人者，无他焉，善推其所为而已矣。", "The reason why the ancients so greatly surpassed other men was no other than this: they were good at extending what they did.")
    lu "[line]"
    voice "vo_lu_root_c5.ogg"
    $ line = t("今恩足以及禽兽，而功不至于百姓者，独何与？", "Now kindness is sufficient to reach to birds and beasts, but the benefit of it does not reach to the people—how is it?")
    lu "[line]"

    jump ga_root_choice

label ga_root_choice:
    scene art25_choice6 with fade
    $ opt_a = t("聆听「葡萄树与枝子」", "Hear: The True Vine")
    $ opt_b = t("聆听「野橄榄与枝子」", "Hear: The Wild Olive Tree")
    $ opt_c = t("聆听「溪水义人」", "Hear: Tree by the Rivers")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump ga_root_a
        "[tag_b]":
            $ wrong_root += 1
            jump ga_root_b
        "[tag_c]":
            $ wrong_root += 1
            jump ga_root_c

label ga_root_a:
    voice "vo_ga_root_a.ogg"
    $ line = t("我是真葡萄树，我父是栽培的人。凡属我不结果子的枝子，他就剪去；", "I am the true vine, and my Father is the husbandman. Every branch in me that beareth not fruit he taketh away:")
    ga "[line]"
    voice "vo_ga_root_a2.ogg"
    $ line = t("凡结果子的，他就修理干净，使枝子结果子更多。", "and every branch that beareth fruit, he purgeth it, that it may bring forth more fruit.")
    ga "[line]"
    voice "vo_ga_root_a6.ogg"
    $ line = t("你们因我讲给你们的道，已经干净了。", "Now ye are clean through the word which I have spoken unto you.")
    ga "[line]"

    voice "vo_ga_root_a3.ogg"
    $ line = t("你们要常在我里面，我也常在你们里面。枝子若不常在葡萄树上，自己就不能结果子；你们若不常在我里面，也是这样。", "Abide in me, and I in you. As the branch cannot bear fruit of itself, except it abide in the vine; no more can ye, except ye abide in me.")
    ga "[line]"
    voice "vo_ga_root_a4.ogg"
    $ line = t("我是葡萄树，你们是枝子。常在我里面的，我也常在他里面，这人就多结果子；因为离了我，你们就不能做什么。", "I am the vine, ye are the branches: He that abideth in me, and I in him, the same bringeth forth much fruit: for without me ye can do nothing.")
    ga "[line]"
    voice "vo_ga_root_a5.ogg"
    $ line = t("人若不常在我里面，就像枝子丢在外面枯干，人拾起来，扔在火里烧了。", "If a man abide not in me, he is cast forth as a branch, and is withered; and men gather them, and cast them into the fire, and they are burned.")
    ga "[line]"
    jump root_settle

label ga_root_b:
    voice "vo_ga_root_b.ogg"
    $ line = t("若有几根枝子被折下来，你这野橄榄得接在其中，一同得着橄榄根的肥汁，你就不可向旧枝子夸口。", "And if some of the branches be broken off, and thou, being a wild olive tree, wert graffed in among them, and with them partakest of the root and fatness of the olive tree; Boast not against the branches.")
    ga "[line]"
    voice "vo_ga_root_b2.ogg"
    $ line = t("若是夸口，当知道不是你托着根，乃是根托着你。", "But if thou boast, thou bearest not the root, but the root thee.")
    ga "[line]"
    voice "vo_ga_root_b4.ogg"
    $ line = t("你若说：「那枝子被折下来，是特为叫我接上。」不错，他们因为不信，所以被折下来；", "Thou wilt say then, The branches were broken off, that I might be graffed in. Well; because of unbelief they were broken off;")
    ga "[line]"

    voice "vo_ga_root_b3.ogg"
    $ line = t("你因为信，所以立得住。你不可自高，反要惧怕。神既不爱惜原来的枝子，也必不爱惜你。", "Thou standest by faith. Be not highminded, but fear. For if God spared not the natural branches, take heed lest he also spare not thee.")
    ga "[line]"
    jump root_settle

label ga_root_c:
    voice "vo_ga_root_c.ogg"
    $ line = t("不从恶人的计谋，不站罪人的道路，不坐亵慢人的座位，惟喜爱耶和华的律法，昼夜思想，这人便为有福。", "Blessed is the man that walketh not in the counsel of the ungodly, nor standeth in the way of sinners, nor sitteth in the seat of the scornful. But his delight is in the law of the Lord; and in his law doth he meditate day and night.")
    ga "[line]"
    voice "vo_ga_root_c2.ogg"
    $ line = t("他要像一棵树栽在溪水旁，按时候结果子，叶子也不枯干。凡他所作的尽都顺利。", "And he shall be like a tree planted by the rivers of water, that bringeth forth his fruit in his season; his leaf also shall not wither; and whatsoever he doeth shall prosper.")
    ga "[line]"
    voice "vo_ga_root_c3.ogg"
    $ line = t("恶人并不是这样，乃像糠秕被风吹散。", "The ungodly are not so: but are like the chaff which the wind driveth away.")
    ga "[line]"
    jump root_settle

    # ========== 判决结果 ==========
label root_settle:
    # 第三审结算：两组三选一，错一组（一半）就判 ♦
    if wrong_root >= 1:
        $ win_root = 0
        jump root_bad
    $ win_root = 1

    voice "vo_narr_038.ogg"
    $ line = t("少年哀叹着，因为他知道自己在这方面存在罪过，但还是想说说几句聊以自慰的话。", "The youth sighed, knowing full well his guilt in this matter, yet still struggling to find words to justify himself.")
    narrator "[line]"

    voice "vo_s_025.ogg"
    $ line = t("是的，是的……但…但我还是爱人类的啊！", "Yes, yes… but… but I do love humanity, don't I?")
    s "[line]"

    voice "vo_s_026.ogg"
    $ line = t("我爱那在酒绿灯红的都市的无人问津的角落里的可怜而不幸的人们；", "I love the poor and unfortunate souls in the forgotten corners of the glittering city.")
    s "[line]"

    voice "vo_s_027.ogg"
    $ line = t("我也悲悯那些在那禾稼不登、饿殍遍野的岁月与国度里的苍白无力死去的人们；", "I pity those who die pale and powerless in years and lands of failed harvests and starving multitudes.")
    s "[line]"

    voice "vo_s_028.ogg"
    $ line = t("我也可怜那些受尽回禄之灾，在煨烬满目的焦黑的土地伫立着的孤苦伶仃，受尽雪虐风饕的受难者……", "I grieve for the lonely, haggard survivors standing in the scorched, ashen earth after fires, suffering the cruelty of snow and storm…")
    s "[line]"

    voice "vo_s_029.ogg"
    $ line = t("这些，怎么能说我脱离人民呢。", "How can you say I am severed from the people?")
    s "[line]"

    voice "vo_narr_039.ogg"
    $ line = t("少年声音渐沉，指尖不自觉地攥紧，他不想止住口，尽管他明知他是在诡辩，是在偷换概念。", "His voice sank lower, his fingers clenching unconsciously. He did not want to stop, though he knew he was quibbling, twisting the meaning of words.")
    narrator "[line]"

    voice "vo_s_030.ogg"
    $ line = t("还有我们的传统，可我又能做些什么呢？", "And our tradition—what am I supposed to do?")
    s "[line]"

    voice "vo_s_031.ogg"
    $ line = t("你们期待的绝不可能是让我在中秋赏花灯、鉴明月，在新春张灯结彩、欢忭鼓舞等等诸如此类的形式上的事……", "You cannot expect me to merely go through the motions: watching lanterns and the moon at Mid-Autumn, hanging lanterns and celebrating at New Year, and all such things…")
    s "[line]"

    voice "vo_s_032.ogg"
    $ line = t("至于那些传统的技艺，途穷末路自会有人花样翻新，它们会浸泡在电子福尔马林的溶剂里，", "As for the traditional crafts, they will be reinvented by someone when their time is done. They will be preserved in the electronic formaldehyde of memory.")
    s "[line]"

    voice "vo_s_033.ogg"
    $ line = t("有人会对它们不屑一顾，有人会把它们奉为圭臬，这是个人的选择，也是时代的选择，可这……", "Some will scorn them, some will revere them. It is a matter of personal choice, and of the choice of the age. But this…")
    s "[line]"

    voice "vo_narr_040.ogg"
    $ line = t("少年的啜泣阻滞了他最后的辩白，他的面部因巨大的痛苦而扭曲抽搐，大滴大滴的泪珠滚落。", "A sob choked his final words. His face twisted with overwhelming pain, and great tears rolled down his cheeks.")
    narrator "[line]"

    voice "vo_narr_041.ogg"
    $ line = t("他继而又叹了口气，哂笑自己的懦弱与无能。", "Then he sighed, laughing bitterly at his own weakness and helplessness.")
    narrator "[line]"

    voice "vo_s_034.ogg"
    $ line = t("等这一切结束了，我也要「走」了吧。", "When this is all over, I suppose I'll go too.")
    s "[line]"

    voice "vo_narr_042.ogg"
    $ line = t("他强抑制自己的泪水，准备聆听对方同样也是最后的控诉。", "he muttered, fighting back the tears, bracing himself for the final condemnation.")
    narrator "[line]"

    jump verdict_start

label root_bad:
    # —— 第三审 ♦：少年不肯认 ——
    scene art23_despair with fade
    voice "vo_s_041.ogg"
    $ line = t("少年（哂笑着）：何以见得我在这方面有过呢？我可是深爱着人类的啊！", "The youth (with a bitter sneer): What grounds are there to say I am at fault in this regard? I hold deep love for humanity!")
    s "[line]"

    voice "vo_s_042.ogg"
    $ line = t("难道我不为那些在酒绿灯红的都市的无人问津的角落里的可怜而不幸的人们而感到悲悯吗？", "Do I not feel compassion for the wretched, unfortunate souls forgotten in the shadow-strewn corners of glittering cities?")
    s "[line]"

    voice "vo_s_043.ogg"
    $ line = t("难道我无法与那些在那禾稼不登、饿殍遍野的岁月与国度里的苍白无力死去的人们共情吗？", "Can I not empathize with those who perish pale and helpless in lands and seasons of failed harvest and widespread famine?")
    s "[line]"

    voice "vo_s_044.ogg"
    $ line = t("难道我不可怜那些受尽回禄之灾，在煨烬满目的焦黑的土地伫立着的孤苦伶仃，受尽雪虐风饕的受难者吗？……凡此种种，怎能说我脱离人民呢。", "Do I not pity the lonely survivors ravaged by fire, standing upon charred, ash-covered ground, tormented by bitter frost and raging gales? … Given all of this, how can you claim I have cut myself off from the people?")
    s "[line]"

    voice "vo_narr_071.ogg"
    $ line = t("少年声音渐沉，他明知自己是在诡辩，是在恬不知耻地偷换概念，但这种想法倏忽间就从他的脑海中烟消云散了。", "The youth's voice sinks low. He knows full well he is quibbling, brazenly twisting concepts, yet this awareness swiftly vanishes from his mind.")
    narrator "[line]"

    voice "vo_s_045.ogg"
    $ line = t("还有，你说我们的传统，可我又能做得了什么呢？", "Then there is what you call our tradition. What could I possibly do about it?")
    s "[line]"

    voice "vo_s_046.ogg"
    $ line = t("难道你们真寄希望于我在中秋赏花灯、鉴明月，在新春张灯结彩、欢忭鼓舞等等诸如此类的形式上的事吗？", "Can you truly expect me to go through empty formalities: admiring lanterns and the bright moon at Mid-Autumn, hanging festive ornaments and rejoicing at the New Year, and the like?")
    s "[line]"

    voice "vo_s_047.ogg"
    $ line = t("……至于那些传统的技艺，途穷末路自是历史与社会的选择，更何况它们并没有消失，它们会浸泡在电子福尔马林的溶剂里，供活人投去付之罔闻的一瞥，供死者残留伤春悲秋的想往……", "… As for the ancient crafts, their decline is the choice of history and society. What is more, they have not perished entirely. They lie preserved in the formaldehyde of electronics, receiving indifferent glances from the living, and nostalgic melancholy longings from the dead…")
    s "[line]"

    voice "vo_s_048.ogg"
    $ line = t("两位圣人，你们可搞错了吧，这是宏大的抉择，怎可怪罪到我头上？", "O two sages, you are mistaken. These are grand, epoch-spanning choices; how can you lay the blame upon my shoulders?")
    s "[line]"

    jump verdict_start

label verdict_start:
    scene art26_look_up with fade
    voice "vo_narr_043.ogg"
    $ line = t("—— 判决结果 ——", "—— The Verdict ——")
    narrator "[line]"

    voice "vo_narr_044.ogg"
    $ line = t("审判结束了，少年缓缓地抬起头，用他那苍白朦胧的目光注视着缥缈的火光中缄默不语着的两位判官。", "The trial was over. The youth slowly lifted his head, his pale, misty gaze fixed on the two silent judges in the wavering firelight.")
    narrator "[line]"

    voice "vo_narr_045.ogg"
    $ line = t("此刻，他已不想再为自己做些无谓的辩护，妄图来挽回自己的声誉与自尊，", "He no longer wished to make empty defenses for himself, to salvage his pride and reputation.")
    narrator "[line]"

    voice "vo_narr_046.ogg"
    $ line = t("他只想知道，他们会怎么判他的罪，他又将何去何从？", "He only wanted to know: what would their verdict be, and where would he go from here?")
    narrator "[line]"

    voice "vo_narr_047.ogg"
    scene art27_walk_out with fade
    $ line = t("在一阵沉默之后，从两位圣徒的身后传出的一阵熟悉而又陌生的脚步声打破了这场阒寂。", "After a long silence, the stillness was broken by the sound of familiar yet strange footsteps from behind the sages.")
    narrator "[line]"

    voice "vo_narr_048.ogg"
    $ line = t("少年惊奇地发现，从后方走来的竟是他自己。那个他脸色庄严肃穆，正目不转睛地注视着自己。", "To the youth's astonishment, he saw himself walking toward him from the shadows. This other self wore a solemn, steady expression, gazing straight at him.")
    narrator "[line]"

    voice "vo_s_035.ogg"
    scene art28_face_to_face with fade
    $ line = t("你也是来审判我的吗？", "Have you also come to judge me?")
    s "[line]"

    voice "vo_narr_049.ogg"
    $ line = t("少年讶异道，他的嗓音发颤，用湿润的目光同样回敬着他。", "the youth whispered, his voice trembling, his wet eyes meeting the gaze of his double.")
    narrator "[line]"

    voice "vo_other_001.ogg"
    $ line = t("不，没有人能够审判他人，即使他被人们顶礼膜拜，被人们崇奉为圣人。", "No. No one can judge another, even if they are revered as sages by the multitudes.")
    other "[line]"

    voice "vo_other_002.ogg"
    $ line = t("你本就清楚这一点。", "You have always known this.")
    other "[line]"

    voice "vo_s_036.ogg"
    $ line = t("诚然，只有我自己能够审判自己。", "Truly, only I can judge myself.")
    s "[line]"

    voice "vo_narr_050.ogg"
    $ line = t("少年幡然憬悟，他若有所思地说。", "The youth realized, thoughtful.")

    narrator "[line]"

    voice "vo_s_037.ogg"
    $ line = t("但我犯下了三重罪孽，难道就能因我是我自己的判官而不了了之吗？", "But I have committed three sins. Can they just be dismissed because I am my own judge?")
    s "[line]"

    voice "vo_s_038.ogg"
    $ line = t("比起一时的自省与尔后前途云泥莫辨，难道予我惩罚以让我对此刻骨铭心不是更好吗？", "Would it not be better to be punished, so that I may never forget?")
    s "[line]"

    voice "vo_other_003.ogg"
    $ line = t("不，你首先正视了自身的问题，这就已足称嘉尚了。", "No. You have first faced the truth of what you are. That in itself is praiseworthy.")
    other "[line]"

    # 孔门儒生三选一
    $ opt_a = t("聆听「晋公知过」", "Hear: Duke Ling Acknowledges Fault")
    $ opt_b = t("聆听「日月之食」", "Hear: Faults Like Eclipses")
    $ opt_c = t("聆听「与人为善」", "Hear: Rejoicing to Hear Faults")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump conf_verdict_a
        "[tag_b]":
            jump conf_verdict_b
        "[tag_c]":
            jump conf_verdict_c

label conf_verdict_a:
    voice "vo_conf_ver_a4.ogg"
    $ line = t("晋灵公不君，厚敛以雕墙，从台上弹人，而观其辟丸也。", "Duke Ling of Jin was no prince. He levied heavy taxes to decorate his walls with carvings. He shot at people from a tower, to see them dodge the pellets.")
    conf "[line]"
    voice "vo_conf_ver_a5.ogg"
    $ line = t("宰夫胹熊蹯不熟，杀之，置诸畚，使妇人载以过朝。", "When his cook failed to stew a bear's paw thoroughly, he put him to death, and ordered the body to be carried out in a basket by women past the court.")
    conf "[line]"
    voice "vo_conf_ver_a6.ogg"
    $ line = t("赵盾、士季见其手，问其故，而患之。", "Zhao Dun and Shi Ji saw the cook's hand, asked the cause, and were grieved.")
    conf "[line]"
    voice "vo_conf_ver_a7.ogg"
    $ line = t("将谏，士季曰：「谏而不入，则莫之继也。会请先，不入，则子继之。」", "They were about to remonstrate with the duke, when Shi Ji said, 'If your remonstrance is not heeded, no one will be able to follow it. Let me go first. If it is of no avail, then you shall follow.'")
    conf "[line]"
    voice "vo_conf_ver_a8.ogg"
    $ line = t("三进及溜，而后视之。曰：「吾知所过矣，将改之。」", "Shi Ji advanced three times, till he came to the eaves of the palace, before the duke saw him. The duke said, 'I know my errors. I will amend them.'")
    conf "[line]"

    voice "vo_conf_ver_a.ogg"
    $ line = t("人谁无过？过而能改，善莫大焉。", "What man is there who errs not? He who errs and can amend is the best of men.")
    conf "[line]"
    voice "vo_conf_ver_a2.ogg"
    $ line = t("《诗》云：「靡不有初，鲜克有终。」夫如是，则能补过者鲜矣。", "It is said in the Book of Poetry, All have a beginning, but few have an end. If this be so, few there are who can amend their faults.")
    conf "[line]"
    voice "vo_conf_ver_a3.ogg"
    $ line = t("君能有终，则社稷之固也，岂惟群臣赖之。", "If your Highness can have this end, the state will be stable indeed. It is not only your ministers who depend on it.")
    conf "[line]"
    voice "vo_conf_ver_a9.ogg"
    $ line = t("又曰：「衮职有阙，惟仲山甫补之。」能补过也。君能补过，衮不废矣。", "It is said again, 'The duties of the sovereign have deficiencies; it is Zhong Shan Fu who supplies them.' That shows that the sovereign can amend his faults. If your Highness can amend your faults, the royal dignity will not be lost.")
    conf "[line]"

    jump monk_verdict_choice

label conf_verdict_b:
    voice "vo_conf_ver_b.ogg"
    $ line = t("过则勿惮改。", "When you have faults, do not fear to amend them.")
    conf "[line]"
    voice "vo_conf_ver_b2.ogg"
    $ line = t("君子之过也，如日月之食焉：过也，人皆见之；更也，人皆仰之。", "The faults of the superior man are like eclipses of the sun and moon. He has his faults, and all men see them; he amends them, and all men look up to him.")
    conf "[line]"
    voice "vo_conf_ver_b4.ogg"
    $ line = t("子夏曰：「小人之过也必文。」", "Zi Xia said, 'The faults of the small man are sure to be glossed over.'")
    conf "[line]"

    voice "vo_conf_ver_b3.ogg"
    $ line = t("吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？", "I daily examine myself on three points: whether, in transacting business for others, I may have been not faithful; whether, in intercourse with friends, I may have been not sincere; whether I may have not mastered and practiced the instructions of my teacher.")
    conf "[line]"
    jump monk_verdict_choice

label conf_verdict_c:
    voice "vo_conf_ver_c.ogg"
    $ line = t("子路，人告之以有过，则喜。禹闻善言，则拜。", "When Zi Lu heard anyone point out a fault to him, he was pleased. When Yu heard a good word, he bowed to the speaker.")
    conf "[line]"
    voice "vo_conf_ver_c2.ogg"
    $ line = t("大舜有大焉：善与人同，舍己从人，乐取于人以为善。", "Great Shun had a still greater excellence: he shared with others what was good; he cast aside his own views, and followed those of others; he delighted to take from others in order to do good.")
    conf "[line]"
    voice "vo_conf_ver_c4.ogg"
    $ line = t("自耕稼、陶、渔以至为帝，无非取于人者。取诸人以为善，是与人为善者也。", "From his earliest days, plowing the ground, making pottery, fishing, till he became emperor, everything he had was taken from others. To take from others and thereby do good is to do good together with others.")
    conf "[line]"

    voice "vo_conf_ver_c3.ogg"
    $ line = t("故君子莫大乎与人为善。", "Therefore the highest excellence of the superior man is this: to do good together with others.")
    conf "[line]"
    jump monk_verdict_choice

label monk_verdict_choice:
    $ opt_a = t("聆听「拉撒路复活」", "Hear: Resurrection of Lazarus")
    $ opt_b = t("聆听「末日启示」", "Hear: The Last Resurrection")
    $ opt_c = t("聆听「血漏妇人」", "Hear: The Woman with the Issue")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump monk_verdict_a
        "[tag_b]":
            jump monk_verdict_b
        "[tag_c]":
            jump monk_verdict_c

label monk_verdict_a:
    voice "vo_monk_ver_a5.ogg"
    $ line = t("有一个患病的人，名叫拉撒路，住在伯大尼，就是马利亚和她姐姐马大的村子。", "Now a certain man was sick, named Lazarus, of Bethany, the town of Mary and her sister Martha.")
    monk "[line]"
    voice "vo_monk_ver_a6.ogg"
    $ line = t("耶稣到了，就知道拉撒路在坟墓里已经四天了。", "Then when Jesus came, he found that he had lain in the grave four days already.")
    monk "[line]"
    voice "vo_monk_ver_a7.ogg"
    $ line = t("马大对耶稣说：「主啊，你若早在这里，我兄弟必不死。就是现在，我也知道，你无论向神求什么，神也必赐给你。」", "Then said Martha unto Jesus, Lord, if thou hadst been here, my brother had not died. But I know, that even now, whatsoever thou shalt ask of God, God will give it thee.")
    monk "[line]"

    voice "vo_monk_ver_a.ogg"
    $ line = t("耶稣对她说：「复活在我，生命在我。信我的人虽然死了，也必复活；", "Jesus said unto her, I am the resurrection, and the life: he that believeth in me, though he were dead, yet shall he live:")
    monk "[line]"
    voice "vo_monk_ver_a2.ogg"
    $ line = t("凡活着信我的人必永远不死。你信这话吗？」", "And whosoever liveth and believeth in me shall never die. Believest thou this?")
    monk "[line]"
    voice "vo_monk_ver_a8.ogg"
    $ line = t("马大说：「主啊，是的，我信你是基督，是神的儿子，就是那要临到世界的。」", "She saith unto him, Yea, Lord: I believe that thou art the Christ, the Son of God, which should come into the world.")
    monk "[line]"
    voice "vo_monk_ver_a9.ogg"
    $ line = t("耶稣又心里悲叹，来到坟墓前。这坟墓是个洞，有一块石头挡着。", "When Jesus therefore saw her weeping, and the Jews also weeping which came with her, he groaned in the spirit, and was troubled. Then Jesus, again groaning in himself, cometh to the grave. It was a cave, and a stone lay upon it.")
    monk "[line]"
    voice "vo_monk_ver_a10.ogg"
    $ line = t("耶稣说：「你们把石头挪开。」", "Jesus said, Take ye away the stone.")
    monk "[line]"
    voice "vo_monk_ver_a11.ogg"
    $ line = t("那死人的姐姐马大对他说：「主啊，他现在必是臭了，因为他死了已经四天了。」", "Martha, the sister of him that was dead, saith unto him, Lord, by this time he stinketh: for he hath been dead four days.")
    monk "[line]"
    voice "vo_monk_ver_a12.ogg"
    $ line = t("耶稣说：「我不是对你说过，你若信，就必看见神的荣耀吗？」", "Jesus saith unto her, Said I not unto thee, that, if thou wouldest believe, thou shouldest see the glory of God?")
    monk "[line]"
    voice "vo_monk_ver_a13.ogg"
    $ line = t("他们就把石头挪开。", "Then they took away the stone from the place where the dead was laid.")
    monk "[line]"
    voice "vo_monk_ver_a3.ogg"
    $ line = t("耶稣举目望天，说：「父啊，我感谢你，因为你已经听我。」", "And Jesus lifted up his eyes, and said, Father, I thank thee that thou hast heard me.")
    monk "[line]"
    voice "vo_monk_ver_a14.ogg"
    $ line = t("我也知道你常听我，但我说这话是为周围站着的众人，叫他们信是你差了我来。", "And I knew that thou hearest me always: but because of the people which stand by I said it, that they may believe that thou hast sent me.")
    monk "[line]"

    voice "vo_monk_ver_a4.ogg"
    $ line = t("说了这话，就大声呼叫说：「拉撒路，出来！」那死人就出来了。", "And when he thus had spoken, he cried with a loud voice, Lazarus, come forth. And he that was dead came forth.")
    monk "[line]"
    voice "vo_monk_ver_a15.ogg"
    $ line = t("手脚裹着布，脸上包着手巾。耶稣对他们说：「解开他，让他走。」", "bound hand and foot with graveclothes: and his face was bound about with a napkin. Jesus saith unto them, Loose him, and let him go.")
    monk "[line]"

    jump youth_amend

label monk_verdict_b:
    voice "vo_monk_ver_b.ogg"
    $ line = t("我实实在在地告诉你们：时候将到，现在就是了，死人要听见神儿子的声音，听见的人就要活了。", "Verily, verily, I say unto you, The hour is coming, and now is, when the dead shall hear the voice of the Son of God: and they that hear shall live.")
    monk "[line]"
    voice "vo_monk_ver_b4.ogg"
    $ line = t("父怎样在自己有生命，就赐给他儿子也照样在自己有生命，并且因为他是人子，就赐给他行审判的权柄。你们不要把这事看作希奇。", "For as the Father hath life in himself; so hath he given to the Son to have life in himself; And hath given him authority to execute judgment also, because he is the Son of man. Marvel not at this:")
    monk "[line]"

    voice "vo_monk_ver_b2.ogg"
    $ line = t("时候要到，凡在坟墓里的，都要听见他的声音，就出来。", "For the hour is coming, in the which all that are in the graves shall hear his voice, And shall come forth;")
    monk "[line]"
    voice "vo_monk_ver_b3.ogg"
    $ line = t("行善的复活得生，作恶的复活定罪。", "they that have done good, unto the resurrection of life; and they that have done evil, unto the resurrection of damnation.")
    monk "[line]"
    jump youth_amend

label monk_verdict_c:
    voice "vo_monk_ver_c4.ogg"
    $ line = t("有一个女人，患了十二年的血漏，在好些医生手里受了许多的苦，又花尽了她所有的，一点也不见好，反倒更重了。", "A certain woman, which had an issue of blood twelve years, And had suffered many things of many physicians, and had spent all that she had, and was nothing bettered, but rather grew worse.")
    monk "[line]"

    voice "vo_monk_ver_c.ogg"
    $ line = t("她听见耶稣的事，就从后头来，杂在众人中间，摸耶稣的衣裳，", "When she had heard of Jesus, she came in the press behind, and touched his garment.")
    monk "[line]"
    voice "vo_monk_ver_c2.ogg"
    $ line = t("心里说：「我只摸他的衣裳，就必痊愈。」于是她血漏的源头立刻干了，她便觉得身上的灾病好了。", "For she said, If I may touch but his clothes, I shall be whole. And straightway the fountain of her blood was dried up; and she felt in her body that she was healed of that plague.")
    monk "[line]"
    voice "vo_monk_ver_c5.ogg"
    $ line = t("耶稣心里知道有能力从自己身上出去，就转过来说：「摸我的是谁？」", "And immediately Jesus, knowing in himself that virtue had gone out of him, turned him about in the press, and said, Who touched my clothes?")
    monk "[line]"
    voice "vo_monk_ver_c6.ogg"
    $ line = t("门徒说：「你看众人拥挤你，还问摸我的是谁吗？」", "And his disciples said unto him, Thou seest the multitude thronging thee, and sayest thou, Who touched me?")
    monk "[line]"
    voice "vo_monk_ver_c7.ogg"
    $ line = t("耶稣周围观看，要见做这事的女人。那女人知道在自己身上所成的事，就恐惧战兢，来俯伏在耶稣跟前，将实情全告诉他。", "And he looked round about to see her that had done this thing. But the woman fearing and trembling, knowing what was done in her, came and fell down before him, and told him all the truth.")
    monk "[line]"

    voice "vo_monk_ver_c3.ogg"
    $ line = t("耶稣对她说：「女儿，你的信救了你，平平安安地去吧！你的灾病痊愈了。」", "And he said unto her, Daughter, thy faith hath made thee whole; go in peace, and be whole of thy plague.")
    monk "[line]"
    jump youth_amend

label youth_amend:
    scene art30_ask with fade
    voice "vo_narr_051.ogg"
    $ line = t("少年意识到了什么，带着渴求询问道。", "The youth realized something, and asked with a voice of longing.")
    narrator "[line]"

    voice "vo_s_039.ogg"
    $ line = t("既然说我意识到了自己的过失，那我该怎么改过呢？", "If I have acknowledged my faults, then how am I to amend them?")
    s "[line]"

    # 鲁鄹邑人三选一
    $ opt_a = t("聆听「诚其意毋自欺」", "Hear: Make the Will Sincere")
    $ opt_b = t("聆听「修身在正其心」", "Hear: Rectifying the Heart")
    $ opt_c = t("聆听「克己复礼」", "Hear: Subdue Oneself, Return to Propriety")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump lu_amend_a
        "[tag_b]":
            jump lu_amend_b
        "[tag_c]":
            jump lu_amend_c

label lu_amend_a:
    voice "vo_lu_amd_a.ogg"
    $ line = t("所谓诚其意者，毋自欺也。如恶恶臭，如好好色，此之谓自谦。", "What is meant by making the will sincere? It means, let there be no self-deception. Let a man dislike badness as he dislikes bad smells, and let him love goodness as he loves beautiful colours.")
    lu "[line]"
    voice "vo_lu_amd_a2.ogg"
    $ line = t("故君子必慎其独也。小人闲居为不善，无所不至，见君子而后厌然，掩其不善而著其善。", "Therefore the superior man must be watchful over himself when he is alone. The small man, when he is at leisure and alone, does nothing but evil. When he sees a superior man, he tries to conceal his evil, and makes a display of his goodness.")
    lu "[line]"
    voice "vo_lu_amd_a3.ogg"
    $ line = t("人之视己，如见其肺肝然，则何益矣？此谓诚于中，形于外。故君子必慎其独也。", "But men see us as we see our own lungs and liver. What is the good of this dissimulation? This is what is meant by saying, What is true within will show itself without. Therefore the superior man must be watchful over himself when he is alone.")
    lu "[line]"
    voice "vo_lu_amd_a4.ogg"
    $ line = t("十目所视，十手所指，其严乎！富润屋，德润身，心广体胖。故君子必诚其意。", "What ten eyes behold, what ten hands point at—how severe is the scrutiny! Riches adorn a house; virtue adorns the person. When the heart is broad and large, the whole frame is at ease. Therefore the superior man must make his will sincere.")
    lu "[line]"
    jump ga_amend_choice

label lu_amend_b:
    voice "vo_lu_amd_b.ogg"
    $ line = t("所谓修身在正其心者：身有所忿懥，则不得其正；有所恐惧，则不得其正；", "What is meant by saying, The cultivation of the person depends on rectifying the heart? If a man be under the influence of passion, he will be wrong in attaining the proper object. If he be under the influence of fear, he will be wrong.")
    lu "[line]"
    voice "vo_lu_amd_b2.ogg"
    $ line = t("有所好乐，则不得其正；有所忧患，则不得其正。", "If he be under the influence of joy and pleasure, he will be wrong. If he be under the influence of sorrow and distress, he will be wrong.")
    lu "[line]"
    voice "vo_lu_amd_b3.ogg"
    $ line = t("心不在焉，视而不见，听而不闻，食而不知其味。此谓修身在正其心。", "When the mind is not present, we look and do not see; we hear and do not understand; we eat and do not know the taste of what we eat. This is what is meant by saying, The cultivation of the person depends on rectifying the heart.")
    lu "[line]"
    jump ga_amend_choice

label lu_amend_c:
    voice "vo_lu_amd_c4.ogg"
    $ line = t("颜渊问仁。", "Yan Yuan asked about perfect virtue.")
    lu "[line]"

    voice "vo_lu_amd_c.ogg"
    $ line = t("克己复礼为仁。一日克己复礼，天下归仁焉。", "To subdue one's self and return to propriety is perfect virtue. If a man can for one day subdue himself and return to propriety, all under heaven will ascribe perfect virtue to him.")
    lu "[line]"
    voice "vo_lu_amd_c2.ogg"
    $ line = t("为仁由己，而由人乎哉？", "Is the practice of perfect virtue from a man himself, or is it from others?")
    lu "[line]"
    voice "vo_lu_amd_c5.ogg"
    $ line = t("颜渊曰：「请问其目。」", "Yan Yuan said, 'I beg to ask the steps of it.'")
    lu "[line]"

    voice "vo_lu_amd_c3.ogg"
    $ line = t("非礼勿视，非礼勿听，非礼勿言，非礼勿动。", "Look not at what is contrary to propriety; speak not what is contrary to propriety; do not what is contrary to propriety.")
    lu "[line]"
    voice "vo_lu_amd_c6.ogg"
    $ line = t("颜渊曰：「回虽不敏，请事斯语矣。」", "Yan Yuan said, 'Slow as I am, I will make it my business to practice this saying.'")
    lu "[line]"

    jump ga_amend_choice

label ga_amend_choice:
    $ opt_a = t("聆听「格拉森群鬼」", "Hear: The Gerasene Demoniac")
    $ opt_b = t("聆听「会堂赶鬼」", "Hear: Demoniac in the Synagogue")
    $ opt_c = t("聆听「大卫认罪祷告」", "Hear: David's Prayer of Repentance")
    $ tag_a, tag_b, tag_c = tag(opt_a), tag(opt_b), tag(opt_c)
    menu:
        "[tag_a]":
            jump ga_amend_a
        "[tag_b]":
            jump ga_amend_b
        "[tag_c]":
            jump ga_amend_c

label ga_amend_a:
    voice "vo_ga_amd_a3.ogg"
    $ line = t("耶稣一下船，就有一个被污鬼附着的人从坟茔里出来迎着他。", "And when he was come out of the ship, immediately there met him out of the tombs a man with an unclean spirit,")
    ga "[line]"
    voice "vo_ga_amd_a4.ogg"
    $ line = t("那人常住在坟茔里，没有人能捆住他，就是铁链也不能，因为人屡次用脚镣和铁链捆锁他，铁链竟被他挣断了，脚镣也被他弄碎了；总没有人能制伏他。", "Who had his dwelling among the tombs; and no man could bind him, no, not with chains: Because that he had been often bound with fetters and chains, and the chains had been plucked asunder by him, and the fetters broken in pieces: neither could any man tame him.")
    ga "[line]"
    voice "vo_ga_amd_a5.ogg"
    $ line = t("他昼夜常在坟茔里和山中喊叫，又用石头砍自己。", "And always, night and day, he was in the mountains, and in the tombs, crying, and cutting himself with stones.")
    ga "[line]"
    voice "vo_ga_amd_a6.ogg"
    $ line = t("他远远地看见耶稣，就跑过去拜他，大声呼叫说：「至高神的儿子耶稣，我与你有什么相干？我指着神恳求你，不要叫我受苦！」", "But when he saw Jesus afar off, he ran and worshipped him, And cried with a loud voice, and said, What have I to do with thee, Jesus, thou Son of the most high God? I adjure thee by God, that thou torment me not.")
    ga "[line]"
    voice "vo_ga_amd_a7.ogg"
    $ line = t("是因耶稣曾吩咐他说：「污鬼啊，从这人身上出来吧。」", "For he said unto him, Come out of the man, thou unclean spirit.")
    ga "[line]"

    voice "vo_ga_amd_a.ogg"
    $ line = t("耶稣问他：「你名叫什么？」回答说：「我名叫『群』，因为我们多的缘故。」", "And he asked him, What is thy name? And he answered, saying, My name is Legion: for we are many.")
    ga "[line]"
    voice "vo_ga_amd_a8.ogg"
    $ line = t("就再三地求耶稣，不要叫他们离开那地方。在那里山坡上，有一大群猪吃食。", "And he besought him much that he would not send them away out of the country. Now there was there nigh unto the mountains a great herd of swine feeding.")
    ga "[line]"
    voice "vo_ga_amd_a9.ogg"
    $ line = t("鬼就央求耶稣说：「求你打发我们往猪群里，附着猪去。」", "And all the devils besought him, saying, Send us into the swine, that we may enter into them.")
    ga "[line]"
    voice "vo_ga_amd_a10.ogg"
    $ line = t("耶稣准了他们，", "And he suffered them.")
    ga "[line]"

    voice "vo_ga_amd_a2.ogg"
    $ line = t("污鬼就出来，进入猪里去。于是那群猪闯下山崖，投在海里，淹死了。", "And the unclean spirits went out, and entered into the swine: and the herd ran violently down a steep place into the sea, and were choked in the sea.")
    ga "[line]"
    voice "vo_ga_amd_a11.ogg"
    $ line = t("猪的数目约有二千。", "And they were about two thousand swine.")
    ga "[line]"

    jump final_settle

label ga_amend_b:
    voice "vo_ga_amd_b3.ogg"
    $ line = t("在会堂里有一个人，被污鬼的精气附着，大声喊叫说：", "And there was in their synagogue a man with an unclean spirit; and he cried out with a loud voice,")
    ga "[line]"
    voice "vo_ga_amd_b4.ogg"
    $ line = t("「唉！拿撒勒的耶稣，我们与你有什么相干？你来灭我们吗？我知道你是谁，乃是神的圣者。」", "Saying, Let us alone; what have we to do with thee, thou Jesus of Nazareth? art thou come to destroy us? I know thee who thou art, the Holy One of God.")
    ga "[line]"

    voice "vo_ga_amd_b.ogg"
    $ line = t("不要作声，从这人身上出来吧！", "Hold thy peace, and come out of him.")
    ga "[line]"
    voice "vo_ga_amd_b2.ogg"
    $ line = t("污鬼叫那人抽了一阵疯，大声喊叫，就出来了。众人都惊讶，彼此对问说：这是什么道理？他用权柄能力吩咐污鬼，污鬼就出来。", "And when the unclean spirit had torn him, and cried with a loud voice, he came out of him. And they were all amazed, saying, What thing is this? for with authority commandeth he even the unclean spirits, and they do obey him.")
    ga "[line]"
    voice "vo_ga_amd_b5.ogg"
    $ line = t("于是耶稣的名声传遍了周围地方。", "And immediately his fame spread abroad into all the region of Galilee round about.")
    ga "[line]"

    jump final_settle

label ga_amend_c:
    voice "vo_ga_amd_c.ogg"
    $ line = t("神啊，求你按你的慈爱怜恤我，按你丰盛的慈悲涂抹我的过犯！", "Have mercy upon me, O God, according to thy lovingkindness: according unto the multitude of thy tender mercies blot out my transgressions.")
    ga "[line]"
    voice "vo_ga_amd_c2.ogg"
    $ line = t("求你将我的罪孽洗除净尽，并洁除我的罪！因为我知道我的过犯，我的罪常在我面前。", "Wash me throughly from mine iniquity, and cleanse me from my sin. For I acknowledge my transgressions: and my sin is ever before me.")
    ga "[line]"
    voice "vo_ga_amd_c4.ogg"
    $ line = t("我向你犯罪，唯独得罪了你，在你眼前行了这恶，以致你责备我的时候显为公义，判断我的时候显为清正。", "Against thee, thee only, have I sinned, and done this evil in thy sight: that thou mightest be justified when thou speakest, and be clear when thou judgest.")
    ga "[line]"
    voice "vo_ga_amd_c5.ogg"
    $ line = t("我是在罪孽里生的，在我母亲怀胎的时候就有了罪。", "Behold, I was shapen in iniquity; and in sin did my mother conceive me.")
    ga "[line]"
    voice "vo_ga_amd_c6.ogg"
    $ line = t("你所喜爱的是内里诚实，你在我隐密处必使我得智慧。", "Behold, thou desirest truth in the inward parts: and in the hidden part thou shalt make me to know wisdom.")
    ga "[line]"
    voice "vo_ga_amd_c7.ogg"
    $ line = t("求你用牛膝草洁净我，我就干净；求你洗涤我，我就比雪更白。", "Purge me with hyssop, and I shall be clean: wash me, and I shall be whiter than snow.")
    ga "[line]"
    voice "vo_ga_amd_c8.ogg"
    $ line = t("求你使我得听欢喜快乐的声音，使你所压伤的骨头可以踊跃。", "Make me to hear joy and gladness; that the bones which thou hast broken may rejoice.")
    ga "[line]"
    voice "vo_ga_amd_c9.ogg"
    $ line = t("求你掩面不看我的罪，涂抹我一切的罪孽。", "Hide thy face from my sins, and blot out all mine iniquities.")
    ga "[line]"

    voice "vo_ga_amd_c3.ogg"
    $ line = t("求你为我造清洁的心，使我里面重新有正直的灵。不要丢弃我，使我离开你的面，不要从我收回你的圣灵。", "Create in me a clean heart, O God; and renew a right spirit within me. Cast me not away from thy presence; and take not thy holy spirit from me.")
    ga "[line]"
    jump final_settle

    # ========== 结局 ==========
label final_settle:
    $ wins = win_material + win_emptiness + win_root
    if wins >= 2:
        jump ending
    jump ending_bad

label ending_bad:
    # ========== 坏结局 ==========
    scene art26_look_up with fade
    voice "vo_bad_001.ogg"
    $ line = t("审判结束了，少年倨傲地抬起头，用他那苍白病态的目光注视着缥缈的火光中缄默不语着的两位判官。", "The trial drew to its close. The youth lifted his head haughtily, his pale, sickly gaze fixed upon the two silent judges amid the wavering fire-light.")
    narrator "[line]"

    voice "vo_bad_002.ogg"
    $ line = t("此刻，他多想乘他们不注意，故相陵轹地逃离这个让他敝虑竭晷的牢狱。", "At this moment, he longed to slip away unseen and flee this prison that had worn his spirit thin.")
    narrator "[line]"

    voice "vo_bad_003.ogg"
    $ line = t("同时，他突然感到疑惑，自己到此处来的目的何在？", "At the same time, a sudden doubt stirred within him: what had even brought him hither?")
    narrator "[line]"

    voice "vo_bad_004.ogg"
    scene art27_walk_out with fade
    $ line = t("在一阵沉默之后，从他的身后传出的一阵熟悉而又陌生的脚步声打破了这场阒寂，少年惊奇地发现，从后方走来的竟是他自己。", "After a spell of silence, familiar yet alien footsteps behind him rent the hush. To the youth's astonishment, it was his own self that stepped forth.")
    narrator "[line]"

    voice "vo_bad_005.ogg"
    $ line = t("那个他正嬉皮笑脸地注视着自己，丝毫不掩盖自己鸷狠狼黠的品行。", "This other-self gazed back at him with a mocking grin, making no attempt to hide his fierce, crafty nature.")
    narrator "[line]"

    voice "vo_bad_006.ogg"
    scene art28_face_to_face with fade
    $ line = t("你是谁？", "Who are you?")
    s "[line]"

    voice "vo_bad_007.ogg"
    $ line = t("少年讶异道，他的嗓音发颤，用恛惶的目光回敬他。", "the youth asked in bewilderment, his voice trembling, returning the stare with disquieted eyes.")
    narrator "[line]"

    voice "vo_bad_008.ogg"
    $ line = t("我是谁并不重要，", "Who I am matters little,")
    other "[line]"

    voice "vo_bad_009.ogg"
    $ line = t("更何况你比谁都清楚。", "What is more, you know full well.")
    other "[line]"

    voice "vo_bad_010.ogg"
    $ line = t("少年幡然憬悟，若有所思地沉默着。", "The youth came to a sudden realisation and lapsed into thoughtful silence.")
    narrator "[line]"

    voice "vo_bad_011.ogg"
    $ line = t("这时，那「另一个」「少年」褊慢肆侮地指着鲁鄹邑人，出言不逊道：", "Then this other youth pointed scornfully toward the Man of Zou from Lu and spoke insolently:")
    narrator "[line]"

    voice "vo_bad_012.ogg"
    $ line = t("此夫鲁国之巧伪人孔丘非邪？为我告之：尔作言造语，妄称文、武，冠枝木之冠，带死牛之胁，多辞缪说，不耕而食，不织而衣，摇唇鼓舌，擅生是非，以迷天下之主，使天下学士不反其本，妄作孝弟，而侥幸于封侯富贵者也。子之罪大极重，疾走归！", "Is not this the crafty hypocrite Kung-chiu of Lu? Tell him from me: You coin speeches and false doctrines, presumptuously invoking King Wen and King Wu. You wear a headdress adorned like branching wood, gird yourself with the ribs of slaughtered oxen. With your abundant fallacious discourses, you eat though you plough not, you wear garments though you weave not. You wag your lips and stir up quarrels, to bewilder the lords of the world. You cause scholars to turn away from their true roots, idly inventing filial piety and fraternal deference, all in hope of winning noble rank and riches. Your crimes are grave beyond measure. Begone and return!")
    other "[line]"

    voice "vo_bad_013.ogg"
    $ line = t("说完，他又指着加利利拿撒勒人道：", "Having spoken, he turned and pointed toward the Man of Nazareth from Galilee:")
    narrator "[line]"

    voice "vo_bad_014.ogg"
    $ line = t("救了别人，不能救自己。他是以色列的王，现在可以从十字架上下来，我们就信他。他倚靠神，神若喜悦他，现在可以救他，因为他曾说：「我是神的儿子。」", "He saved others; himself he cannot save. If he be the King of Israel, let him now come down from the cross, and we will believe him. He trusted in God; let him deliver him now, if he will have him: for he said, I am the Son of God.")
    other "[line]"

    voice "vo_bad_015.ogg"
    $ line = t("……", "……")
    narrator "[line]"

    voice "vo_bad_016.ogg"
    scene art31_leave with fade
    $ line = t("从那座敝旧的小屋飞出，少年感到神清气爽，为自己与那两位所谓圣贤唇枪舌剑而逞奸自快。", "He burst forth out of that weather-beaten cottage, feeling light-hearted, exulting in his sharp-tongued victory over those so-called sages.")
    narrator "[line]"

    voice "vo_bad_017.ogg"
    scene art32_look_back with fade
    $ line = t("它回头望向那座还不曾离远的小屋，发现此刻他曾对其出言不逊的两位出现在大门口，扼腕兴叹，凝神注视着它。最后哀叹道：", "He glanced back toward the cottage not yet far behind him, and saw the two he had insulted standing in the doorway. They sighed with grief, their gaze fixed upon him. At last they uttered their lament:")
    narrator "[line]"

    voice "vo_bad_018.ogg"
    $ line = t("古者民有三疾，今也或是之亡也。古之狂也肆，今之狂也荡；古之矜也廉，今之矜也忿戾；古之愚也直，今之愚也诈而已矣。", "Anciently, men had three failings, which now perhaps are not to be found. The high-mindedness of antiquity showed itself in a disregard of small things; the high-mindedness of the present day shows itself in wild license. The stern dignity of antiquity showed itself in grave reserve; the stern dignity of the present day shows itself in quarrelsome perverseness. The stupidity of antiquity showed itself in straightforwardness; the stupidity of the present day shows itself in sheer deceit.")
    lu "[line]"

    voice "vo_bad_019.ogg"
    $ line = t("地上虔诚人灭尽；世间没有正直人；各人埋伏，要杀人流血，都用网罗猎取弟兄。", "The good man is perished out of the earth: and there is none upright among men: they all lie in wait for blood; they hunt every man his brother with a net.")
    ga "[line]"

    voice "vo_bad_020.ogg"
    $ line = t("呵，", "Hah,")
    s "[line]"

    voice "vo_bad_021.ogg"
    scene art34_run_dark with fade
    $ line = t("少年冷笑道，望着前方沉沉的黝黯，玄冥杳暗吞噬着它的躯壳，也吞噬着它的魂灵。随后又低头沉思：", "the youth sneered, gazing into the heavy blackness ahead. The obscure endless gloom swallowed his frame, and swallowed his very soul. Then he bowed his head and pondered.")
    narrator "[line]"

    voice "vo_bad_022.ogg"
    $ line = t("这是梦。", "This is a dream.")
    s "[line]"

    voice "vo_bad_023.ogg"
    $ line = t("它得出结论道，或许会是梦里随后的半途跌跤而惊悸，或许会是晨曦机械的闹钟的轰鸣……总之，这不过的黄粱一梦，是修普洛斯的奥义罢了……", "he concluded. Perhaps he would start awake with a fright mid-fall within this dream. Or perhaps the cold blare of the morning alarm would rouse him… In any case, it was nothing but a millet-dream, the secret wisdom of Hypnos…")
    narrator "[line]"

    voice "vo_bad_024.ogg"
    $ line = t("想到此时，少年又狂妄地枭笑起来，纵身朝远处混沌的黑暗中奔去……", "With that thought, the youth let out another wild, arrogant laugh and sprang forward, running deep into the chaotic darkness afar……")
    narrator "[line]"

    scene black with fade
    stop music fadeout 2.0

    return

label ending:
    scene art31_leave with fade
    voice "vo_narr_052.ogg"
    $ line = t("从那座敝旧的小屋走出，少年容光焕发，他感到神清气爽。", "When the youth stepped out of the weathered cottage, his face was aglow and his spirit felt light and unburdened.")
    narrator "[line]"

    voice "vo_narr_053.ogg"
    $ line = t("他洗心革面，决定从今以后改正自己的罪孽，重新为人。", "He had turned over a new leaf, resolved to mend his ways and be born anew from that day forward.")
    narrator "[line]"

    voice "vo_narr_054.ogg"
    $ line = t("他脑海里浮现出自己革新后的新面貌、新人格，觉得自己芳途坦霁、星衢坦阔。", "In his mind's eye, the vision of his renewed self, his whole new character, unfolded before him, and he felt his path stretching out clear and bright.")
    narrator "[line]"

    voice "vo_narr_055.ogg"
    scene art32_look_back with fade
    $ line = t("他回头望向那座还不曾离远的小屋，发现曾与自己唇枪舌剑的两位圣贤此刻出现在大门口，注视着他。", "He glanced back over his shoulder at the cottage, not yet far behind him, and caught sight of the two sages standing in the doorway, their eyes fixed on him.")
    narrator "[line]"

    voice "vo_narr_056.ogg"
    $ line = t("见少年回头，他们最后嘱愿道：", "As he met their gaze, they spoke their final charge:")
    narrator "[line]"

    voice "vo_lu_end.ogg"
    $ line = t("志士仁人，无求生以害仁，有杀身以成仁。", "The determined scholar and the man of virtue will not seek to live at the expense of injuring virtue. They will even lay down their lives in order to complete their virtue.")
    lu "[line]"

    voice "vo_ga_end.ogg"
    $ line = t("一粒麦子不落在地里死了，仍旧是一粒；若是死了，就结出许多子粒来。", "Verily, verily, I say unto you, Except a corn of wheat fall into the ground and die, it abideth alone: but if it die, it bringeth forth much fruit.")
    ga "[line]"

    voice "vo_narr_057.ogg"
    $ line = t("少年含情脉脉地注视着他们，默默地把他们的所言所语镌之于心。", "The youth held their gaze for a long, quiet moment, every word sinking deep and engraving itself upon his heart.")
    narrator "[line]"

    voice "vo_narr_058.ogg"
    scene art33_field with fade
    $ line = t("然后默默地转身，向远处的旷野奔去……", "Then he turned silently, and set off running toward the wide, distant wilderness…")
    narrator "[line]"

    scene black with fade
    stop music fadeout 2.0

    return
