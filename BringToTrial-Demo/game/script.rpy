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

# ---------- 角色定义 ----------
define narrator = Character(None)
define s = Character("[s_name]", color="#cccccc")
define lu = Character("[lu_name]", color="#d4a574")
define ga = Character("[ga_name]", color="#87ceeb")
define conf = Character("[conf_name]", color="#c9a86c")
define monk = Character("[monk_name]", color="#93b7e3")
define unknown = Character("???", color="#888888")
define other = Character("[other_name]", color="#e0b0ff")

# ---------- 演示版美术（豆包生成，覆盖第一审 第1-65页） ----------
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
    $ line = t("【故事梗概】\n\n铁门之内，那两位被亿万人顶礼膜拜的圣人——鲁鄹邑人与加利利拿撒勒人——正在等他。\n少年不信他们那套旧道理，只想用自己时代的智慧把他们驳倒。\n于是他等来的不是辩论，而是一场审判：先问物质，再问虚无，最后问那道谁也绕不开的道。\n而自始至终，被审判的都是他自己。", "【Synopsis】\n\nBehind the iron gate, two men revered by countless millions — the Man of Zou and the Man of Nazareth — are waiting for him.\nThe youth does not believe a word of their old teaching, and means to refute them with the wisdom of his own age.\nSo what awaits him is not a debate but a trial: first materialism, then emptiness, and at last the one question no one can walk around.\nAnd all along, he is the one on trial.")
    centered "[line]"

    scene art01_entry with fade

    # ========== 开场 ==========
    $ line = t("少年推开那座沉重的铁门，屋内磬静的黢黑刹时吞噬了他那渺小的身躯。", "The youth pushed open the heavy iron gate, and the profound, silent darkness within swallowed his frail frame in an instant.")
    narrator "[line]"

    $ line = t("少年眯起双眼，极力想看清屋内的情状，但除了远处的几朵飘忽不定的幽火以外，其余的一切全被漆上了一层浓稠的黑。", "He narrowed his eyes, straining to make out the interior. Yet save for a few wandering, ghostly flames flickering in the distance, all else was drowned in a thick, viscous gloom.")
    narrator "[line]"

    scene art02_walk with fade
    $ line = t("怀着难以抑制的好奇与恐惧，少年蹀躞徐行，向远处揜菼的灯火趋近。", "Driven by a mingled thrill of curiosity and dread, he paced slowly forward, stepping softly toward the distant, wavering light.")
    narrator "[line]"

    $ line = t("倏忽，他听到了两个浑厚沉雄的声音。起初声音微渺，时断时续。少年停步，侧耳细听：", "Suddenly, two deep, sonorous voices reached his ears. At first they were faint, broken and intermittent. He halted, tilting his head to listen more closely:")
    narrator "[line]"

    $ line = t("世衰道微，邪说暴行有作，臣弑其君者有之，子弑其父者有之。", "When the world declined, and true principles fell into disuse, perverse doctrines and violent deeds arose. There were instances of ministers murdering their sovereigns, and sons murdering their fathers.")
    unknown "[line]"

    $ line = t("邪说诬民，充塞仁义也。仁义充塞，则率兽食人，人将相食。吾为此惧，闲先圣之道，距杨墨，放淫辞，邪说者不得作。", "Such perverse doctrines delude the people, and block up the path of benevolence and righteousness. When benevolence and righteousness are thus blocked up, it is as if men were leading beasts to devour men, and they will be found devouring one another. I am alarmed at these things, and therefore defend the ways of the ancient sages, opposing Yang and Mo, and setting aside licentious speeches.")
    unknown "[line]"

    $ line = t("作于其心，害于其事；作于其事，害于其政。圣人复起，不易吾言矣。", "What arises in the mind, works injuriously on affairs; what works injuriously on affairs, works injuriously on government. Were a sage to arise again, he would not change my words.")
    unknown "[line]"

    $ line = t("第三位天使吹号，就有烧着的大星，好像火把从天上落下来，落在江河的三分之一和众水的泉源上。", "And the third angel sounded, and there fell a great star from heaven, burning as it were a lamp, and it fell upon the third part of the rivers, and upon the fountains of waters;")
    unknown "[line]"

    $ line = t("这星名叫「茵陈」。众水的三分之一变为茵陈；因水变苦，就死了许多人。", "And the name of the star is called Wormwood: and the third part of the waters became wormwood; and many men died of the waters, because they were made bitter.")
    unknown "[line]"

    $ line = t("谈话声音戛然而止。少年覃思罔悟，对刚才谈话的二人及其言语愈发感到好奇，便加快步调向那灯火处走去。", "The voices ceased abruptly. Puzzled and increasingly curious about the two speakers and their words, the youth quickened his pace toward the light.")
    narrator "[line]"

    scene art03_meet_sages with fade
    $ line = t("终于，在火光的尽头，他看见了那两个他既熟稔而又陌生的人：", "At last, at the end of the glow, he beheld the two figures, at once familiar and strange to him:")
    narrator "[line]"

    scene art04_confucius with fade
    $ line = t("其中一人身形高大，头顶微凹，面容庄重，衣饰朴素，带有几分栉风沐雨的憔悴感；", "One was tall of stature, with a slightly sunken crown, a solemn countenance, and plain robes, bearing the weariness of one who had journeyed far and endured much.")
    narrator "[line]"

    scene art05_west_sage with fade
    $ line = t("另一人的样貌普通平凡，无夺目美貌，但神色柔和而坚定，脸上显出一种饱经风霜的质感。", "The other was of common, unremarkable appearance, with no striking beauty, yet his gaze was gentle and steadfast, his face marked with the texture of a life seasoned by trials.")
    narrator "[line]"

    scene art06_two_sages with fade
    $ line = t("少年大骇，因为他一眼便认出了前者正是那鲁鄹邑人，而后者则是加利利拿撒勒人。", "The youth started, for he recognized at once the former as the Man of Zou from Lu, and the latter as the Man of Nazareth from Galilee.")
    narrator "[line]"

    $ line = t("「他们在这里干嘛呢？」少年心想，但不知为何，他油然生出了一种乖戾的想法：", "\"What are they doing here?\" he thought. Yet for some reason, a perverse notion rose within him:")
    narrator "[line]"

    $ line = t("他想用自己的智慧驳倒这两位德高年劭、被芸芸众生顶礼膜拜的圣人。", "he would use his own wits to refute these two sages, revered and worshipped by multitudes.")
    narrator "[line]"

    scene art07_sweet_smile with fade
    $ line = t("「他们那些胶柱鼓瑟的旧思想怎么能胜过我们的新思想呢？」少年露出一丝甜腻腻的微笑，迈步向他们走去。", "\"How can their rigid, outdated old ideas ever prevail against the thinking of our time?\" A faint, smug smile tugged at his lips as he stepped toward them.")
    narrator "[line]"

    $ line = t("喂，那个鄹邑的，还有那个加利利的，你们在这干嘛？", "Ho there, you of Zou, and you of Galilee. What are you doing here?")
    s "[line]"

    $ line = t("少年强装出一副恭维的笑容，尽管他知道他那放荡无理的言语已经无法掩盖他那鬼迷心窍的意志了。", "he called, forcing a smile of feigned deference, though he knew his reckless, insolent words could no longer hide his defiant, mischief-bound resolve.")
    narrator "[line]"

    scene art08_scholar with fade
    $ line = t("为了审判你！", "To judge you!")
    conf "[line]"

    scene art09_monk with fade
    $ line = t("在两位圣人身后的两侧分别走出了一位孔门儒生与一位苦行修士司祭，他们神色凛然，异口同声地说道。", "From either side behind the two sages stepped forth a Confucian Scholar and an Ascetic Monk Priest, their countenances stern, speaking as one.")
    narrator "[line]"

    $ line = t("审判…我？", "Judge… me?")
    s "[line]"

    scene art10_shock_to_smile with fade
    $ line = t("少年错愕不已，但很快又恢复了镇定，脸上又重现出他方才糊上的笑。", "The youth was taken aback, but quickly recovered his composure, the earlier smile returning to his face.")
    narrator "[line]"

    $ line = t("你们凭何来审判我，我何罪之有？", "By what right do you judge me? What sin have I committed?")
    s "[line]"

    $ line = t("他歪着脑袋，详装思索，抹了露出一层哂意：", "He tilted his head, feigning thought, a flicker of mockery playing across his features.")
    narrator "[line]"

    $ line = t("是因为我没能践行你们儒家的准则呢，还是因为我不信基督？", "Is it that I have failed to live by your Confucian rules? Or because I do not believe in Christ?")
    s "[line]"

    $ line = t("两位圣贤正襟危坐，一言不发；从他们身后走到侧旁的孔门儒生与苦行修士司祭也正色凛然地望着他。", "The two sages sat upright and silent, while the Confucian Scholar and the Ascetic Monk Priest, having stepped to their sides, gazed at him with solemn gravity.")
    narrator "[line]"

    scene art11_inner_anger with fade
    $ line = t("少年感到诧异，心里陡地生起一股无名火：", "The youth, surprised, felt a surge of unprovoked anger rise in his chest.")
    narrator "[line]"

    scene art12_disdain with fade
    $ line = t("你们既要审判我，那便来吧！无需装神弄鬼，法官们。", "If you mean to judge me, then get on with it! No need for all this mystic posturing, judges.")
    s "[line]"

    # ========== 第一审：物质 ==========
    $ line = t("—— 第一审：物质 ——", "—— First Trial: Materialism ——")
    narrator "[line]"

    $ line = t("说我物质？你们难道不是在空谈道义？", "You call me materialistic? Is it not you who prattle on empty about morality and virtue?")
    s "[line]"

    $ line = t("没有果腹的食粮，人连立身都难，还谈什么精神操守？", "Without bread to fill the belly, a man can scarce stand on his own two feet—what use are spiritual principles then?")
    s "[line]"

    $ line = t("整个社会都在看重利益、讲求实效，我又有何不对之处？", "The whole world prizes profit and results. What wrong is there in that?")
    s "[line]"

    $ line = t("这世道波诡云谲，惟物质才是底气，惟钱财才有选择。", "In this treacherous, shifting world, only substance gives security, only wealth gives choice.")
    s "[line]"

    $ line = t("你们所谓的德行仁义、安贫乐道，你们所谓的甚于面包的石头岂能饱食终日，能遮风挡雨吗？", "Can your so-called virtue and benevolence, your praise of poverty and contentment—can your stones that are more than bread ever fill a stomach, or shelter a man from the wind and rain?")
    s "[line]"

    $ line = t("与其抱着空原则受苦受穷，不如凭本事挣来实打实的好日子。", "Rather than cling to empty principles and suffer in poverty, I would earn a solid, tangible good life by my own ability.")
    s "[line]"

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
            jump lu_material_b
        "[tag_c]":
            jump lu_material_c

label lu_material_a:
    $ line = t("君子先慎乎德。有德此有人，有人此有土，有土此有财，有财此有用。", "The superior man bends his attention to the cultivation of his virtue. When virtue is there, people will come; when people are there, there will be territory; when there is territory, there will be wealth; when there is wealth, there will be the means of use.")
    lu "[line]"
    $ line = t("德者，本也；财者，末也。外本内末，争民施夺。", "Virtue is the root; wealth is the fruit. When the root is neglected and the fruit is sought after, the people will be stirred up to contention and rapine.")
    lu "[line]"
    $ line = t("是故财聚则民散，财散则民聚。是故言悖而出者，亦悖而入；货悖而入者，亦悖而出。", "Hence, when wealth is gathered together, the people are scattered; when wealth is scattered, the people are gathered together. Hence, when words go forth contrary to reason, they will return contrary to reason; when wealth comes in contrary to reason, it will depart contrary to reason.")
    lu "[line]"
    $ line = t("《康诰》曰：「惟命不于常。」道善则得之，不善则失之矣。", "The Announcement to Kang says, The decree is not always the same. Good conduct obtains it; bad conduct loses it.")
    lu "[line]"
    jump ga_material_choice

label lu_material_b:
    $ line = t("王何必曰利？亦有仁义而已矣。", "Why must your Majesty use that word profit? What I have are benevolence and righteousness, and these are my only themes.")
    lu "[line]"
    $ line = t("王曰「何以利吾国」？大夫曰「何以利吾家」？士庶人曰「何以利吾身」？", "If your Majesty says, What will profit my kingdom? the great officers will say, What will profit my family? and the scholars and common people will say, What will profit myself?")
    lu "[line]"
    $ line = t("上下交征利而国危矣。苟为后义而先利，不夺不餍。", "Superiors and inferiors will thus strive together after profit, and the kingdom will be endangered. But if righteousness be put last, and profit be put first, they will not be satisfied without grasping the whole.")
    lu "[line]"
    $ line = t("未有仁而遗其亲者也，未有义而后其君者也。", "Never has there been benevolence in whose heart the love of his parents was wanting. Never has there been righteousness in whose heart regard to his prince was wanting.")
    lu "[line]"
    jump ga_material_choice

label lu_material_c:
    $ line = t("生财有大道：生之者众，食之者寡，为之者疾，用之者舒，则财恒足矣。", "There is a great way for the production of wealth: let the producers be many, and the consumers few; let the workers be active, and the spenders moderate; then wealth will always be sufficient.")
    lu "[line]"
    $ line = t("仁者以财发身，不仁者以身发财。", "The benevolent man makes wealth advance his person; the unbenevolent man makes his person advance wealth.")
    lu "[line]"
    $ line = t("孟献子曰：「畜马乘，不察于鸡豚；伐冰之家，不畜牛羊；百乘之家，不畜聚敛之臣。与其有聚敛之臣，宁有盗臣。」", "Meng Xian said, A minister who keeps horses and chariots will not look after poultry and pigs. A family that has stores of ice will not rear oxen and sheep. A family of a hundred chariots will not keep a minister to scrape together wealth. It is better to have a minister who robs the state, than one who scrapes together wealth.")
    lu "[line]"
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
            jump ga_material_a
        "[tag_b]":
            jump ga_material_b
        "[tag_c]":
            jump ga_material_c

label ga_material_a:
    $ line = t("不要为自己积攒财宝在地上，地上有虫子咬，能锈坏，也有贼挖窟窿来偷；", "Lay not up for yourselves treasures upon earth, where moth and rust doth corrupt, and where thieves break through and steal:")
    ga "[line]"
    $ line = t("只要积攒财宝在天上，天上没有虫子咬，不能锈坏，也没有贼挖窟窿来偷。", "But lay up for yourselves treasures in heaven, where neither moth nor rust doth corrupt, and where thieves do not break through nor steal:")
    ga "[line]"
    $ line = t("因为你的财宝在哪里，你的心也在哪里。", "For where your treasure is, there will your heart be also.")
    ga "[line]"
    jump youth_material_rebut

label ga_material_b:
    $ line = t("有一个财主，田产丰盛，自己心里思想说：「我的出产没有地方收藏，怎么办呢？」", "The ground of a certain rich man brought forth plentifully: And he thought within himself, saying, What shall I do, because I have no room where to bestow my fruits?")
    ga "[line]"
    $ line = t("又说：「我要这么办：要把我的仓房拆了，另盖更大的，在那里收藏我一切的粮食和财物，", "And he said, This will I do: I will pull down my barns, and build greater; and there will I bestow all my fruits and my goods.")
    ga "[line]"
    $ line = t("然后要对我的灵魂说：灵魂哪，你有许多财物积存，可作多年的费用，只管安安逸逸地吃喝快乐吧！」", "And I will say to my soul, Soul, thou hast much goods laid up for many years; take thine ease, eat, drink, and be merry.")
    ga "[line]"
    $ line = t("神却对他说：「无知的人哪，今夜必要你的灵魂，你所预备的要归谁呢？」", "But God said unto him, Thou fool, this night thy soul shall be required of thee: then whose shall those things be, which thou hast provided?")
    ga "[line]"
    $ line = t("凡为自己积财，在神面前不富足的，也是这样。", "So is he that layeth up treasure for himself, and is not rich toward God.")
    ga "[line]"
    jump youth_material_rebut

label ga_material_c:
    $ line = t("我实在告诉你们，财主进天国是难的。", "Verily I say unto you, That a rich man shall hardly enter into the kingdom of heaven.")
    ga "[line]"
    $ line = t("我又告诉你们，骆驼穿过针的眼，比财主进神的国还容易呢。", "And again I say unto you, It is easier for a camel to go through the eye of a needle, than for a rich man to enter into the kingdom of God.")
    ga "[line]"
    $ line = t("在人这是不能的，在神凡事都能。", "With men this is impossible; but with God all things are possible.")
    ga "[line]"
    jump youth_material_rebut

label youth_material_rebut:
    scene art15_wild_laugh with fade
    $ line = t("少年放肆地笑道，眼里闪烁着轻蔑与挑衅。", "The youth laughed wildly, scorn and defiance flashing in his eyes.")
    narrator "[line]"

    $ line = t("所以说，归根结底，你们不还是不厌其烦地老调重弹着这些陈词滥调吗？", "So after all, you are just harping on the same old tired platitudes, aren't you?")
    s "[line]"

    $ line = t("表面上满是「君子」与「德」、「蔑财」与「心」，实际上也还是满嘴胡吣！", "All this talk of gentleman and virtue, of despising wealth and the heart—it is all nothing but empty words!")
    s "[line]"

    $ line = t("文犹质也，质犹文也。虎豹之鞟犹犬羊之鞟。", "Ornament is as the substance; the substance is as ornament. The skins of a tiger or a leopard stripped of their hair are no different from the skins of a dog or a sheep.")
    conf "[line]"

    $ line = t("此乃「加利利的迦拿之酒」。", "This is the wine of Cana in Galilee.")
    monk "[line]"

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
            jump conf_material_b
        "[tag_c]":
            jump conf_material_c

label conf_material_a:
    $ line = t("孔子迁于蔡三岁，吴伐陈。楚救陈，军于城父。闻孔子在陈蔡之间，楚使人聘孔子。", "Confucius had been in Cai for three years, when Wu invaded Chen. Chu came to the relief of Chen. Hearing that Confucius was between Chen and Cai, the prince of Chu sent messengers to invite him.")
    conf "[line]"
    $ line = t("陈蔡大夫谋曰：「孔子贤者，所刺讥皆中诸侯之疾。今楚，大国也，来聘孔子。孔子用于楚，则陈蔡用事大夫危矣。」", "The great officers of Cai and Chen took counsel together, saying, Confucius is a man of virtue. If he should be employed in Chu, then we, the great officers of Chen and Cai, should be in danger.")
    conf "[line]"
    $ line = t("于是乃相与发徒役围孔子于野。不得行，绝粮。从者病，莫能兴。", "Thereupon they jointly sent out their followers to surround Confucius in the wilderness. He could not proceed, and his supplies of food were exhausted. His followers became ill, and were not able to rise.")
    conf "[line]"
    $ line = t("孔子讲诵弦歌不衰。子路愠见曰：「君子亦有穷乎？」", "But Confucius continued to teach, and chant, and string his lute without ceasing. Zi Lu, full of displeasure, came to him and said, Has the superior man indeed to endure such distress?")
    conf "[line]"
    $ line = t("孔子曰：「君子固穷，小人穷斯滥矣。」", "Confucius said, The superior man maintains his firmness in distress; the small man, when in distress, gives way to unbridled license.")
    conf "[line]"
    jump monk_material_choice

label conf_material_b:
    $ line = t("楚昭王将以书社地七百里封孔子。楚令尹子西曰：「王之使使诸侯有如子贡者乎？」曰：「无有。」", "King Zhao of Chu was about to give Confucius the territory of seven hundred li. But Zi Xi, the chief minister of Chu, said to him, Has your Majesty any ambassador to the princes like Zi Gong? No, was the reply.")
    conf "[line]"
    $ line = t("「王之辅相有如颜回者乎？」曰：「无有。」「王之将率有如子路者乎？」曰：「无有。」", "Has your Majesty any minister to assist you like Yan Hui? No. Has your Majesty any general like Zi Lu? No.")
    conf "[line]"
    $ line = t("「今孔丘述三五之法，明周召之业，王若用之，则楚安得世世堂堂方数千里乎？」", "Now Confucius is setting forth the ways of the Three Kings and Five Lords. If your Majesty employ him, how shall Chu go on to possess its territory of thousands of li square, from generation to generation?")
    conf "[line]"
    $ line = t("昭王乃止。", "On this King Zhao desisted.")
    conf "[line]"
    jump monk_material_choice

label conf_material_c:
    $ line = t("子路问君子。子曰：「修己以安人。」", "Zi Lu asked what constituted a superior man. The Master said, He cultivates himself so as to be in a state of respectful carefulness.")
    conf "[line]"
    $ line = t("曰：「如斯而已乎？」曰：「修己以安百姓。修己以安百姓，尧舜其犹病诸？」", "And is that all? said Zi Lu. He cultivates himself so as to give rest to all the people. To cultivate himself so as to give rest to all the people—even Yao and Shun would have found this a difficult task.")
    conf "[line]"
    $ line = t("原壤夷俟。子曰：「幼而不孙弟，长而无述焉，老而不死，是为贼。」以杖叩其胫。", "Yuan Rang waited for him in a squatting posture. The Master said to him, In youth, you showed no respect to your elders; in manhood, you have achieved nothing; in old age, you go on living and do not die: you are a thief. And with his staff he tapped his leg.")
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
            jump monk_material_a
        "[tag_b]":
            jump monk_material_b
        "[tag_c]":
            jump monk_material_c

label monk_material_a:
    $ line = t("当时，耶稣被圣灵引到旷野，受魔鬼的试探。他禁食四十昼夜，后来就饿了。", "Then was Jesus led up of the Spirit into the wilderness to be tempted of the devil. And when he had fasted forty days and forty nights, he was afterward an hungred.")
    monk "[line]"
    $ line = t("那试探人的进前来，对他说：「你若是神的儿子，可以吩咐这些石头变成食物。」", "And when the tempter came to him, he said, If thou be the Son of God, command that these stones be made bread.")
    monk "[line]"
    $ line = t("耶稣却回答说：「经上记着说：『人活着，不是单靠食物，乃是靠神口里所出的一切话。』」", "But he answered and said, It is written, Man shall not live by bread alone, but by every word that proceedeth out of the mouth of God.")
    monk "[line]"
    $ line = t("魔鬼又带他上了一座最高的山，将世上的万国与万国的荣华都指给他看，", "Again, the devil taketh him up into an exceeding high mountain, and sheweth him all the kingdoms of the world, and the glory of them;")
    monk "[line]"
    $ line = t("对他说：「你若俯伏拜我，我就把这一切都赐给你。」", "And saith unto him, All these things will I give thee, if thou wilt fall down and worship me.")
    monk "[line]"
    $ line = t("耶稣说：「撒但，退去吧！因为经上记着说：『当拜主你的神，单要事奉他。』」", "Then saith Jesus unto him, Get thee hence, Satan: for it is written, Thou shalt worship the Lord thy God, and him only shalt thou serve.")
    monk "[line]"
    $ line = t("于是魔鬼离了耶稣，有天使来伺候他。", "Then the devil leaveth him, and, behold, angels came and ministered unto him.")
    monk "[line]"
    jump material_end

label monk_material_b:
    $ line = t("所以我告诉你们：不要为生命忧虑吃什么，喝什么；为身体忧虑穿什么。", "Therefore I say unto you, Take no thought for your life, what ye shall eat, or what ye shall drink; nor yet for your body, what ye shall put on.")
    monk "[line]"
    $ line = t("生命不胜于饮食吗？身体不胜于衣裳吗？", "Is not the life more than meat, and the body than raiment?")
    monk "[line]"
    $ line = t("你们看天上的飞鸟，也不种，也不收，也不积蓄在仓里，你们的天父尚且养活它。你们不比飞鸟贵重得多吗？", "Behold the fowls of the air: for they sow not, neither do they reap, nor gather into barns; yet your heavenly Father feedeth them. Are ye not much better than they?")
    monk "[line]"
    $ line = t("你们哪一个能用思虑使寿数多加一刻呢？", "Which of you by taking thought can add one cubit unto his stature?")
    monk "[line]"
    jump material_end

label monk_material_c:
    $ line = t("不要爱世界和世界上的事。人若爱世界，爱父的心就不在他里面了。", "Love not the world, neither the things that are in the world. If any man love the world, the love of the Father is not in him.")
    monk "[line]"
    $ line = t("因为凡世界上的事，就像肉体的情欲，眼目的情欲，并今生的骄傲，都不是从父来的，乃是从世界来的。", "For all that is in the world, the lust of the flesh, and the lust of the eyes, and the pride of life, is not of the Father, but is of the world.")
    monk "[line]"
    $ line = t("这世界和其上的情欲都要过去，惟独遵行神旨意的，是永远常存。", "And the world passeth away, and the lust thereof: but he that doeth the will of God abideth for ever.")
    monk "[line]"
    jump material_end

label material_end:
    scene art17_realize with fade
    $ line = t("少年沉思了一阵，他觉得自己理解得过于肤浅，而当他领悟到其中蕴意后，赧颜汗下。", "The youth fell silent, pondering. He had thought his own understanding shallow, but as the meaning of the words dawned on him, a flush of shame burned across his face.")
    narrator "[line]"

    $ line = t("以前，他总觉得他对物质生活孜孜以求，精神上的富足便会悄然而至。", "Once he had thought that if he strove ceaselessly for material comfort, spiritual fulfillment would follow of its own accord.")
    narrator "[line]"

    $ line = t("直到他面对现实时，自己对物质利益锱铢必较，对优越的住房、富足的餐饮、成功的事业也如他人般趋之若鹜。", "But when he faced the truth, he saw how he had haggled over every trivial gain, how he had coveted fine houses, rich food, and worldly success just like everyone else.")
    narrator "[line]"

    $ line = t("他也曾幻想着独属自己的罗特希尔德思想，可到头来却总感到一种心灵上的寂寥与空荡，感到自己迷失了什么……", "He had once dreamed of a Rothschild-like fortune of his own, yet in the end he always felt a hollow emptiness in his soul, as if something were lost…")
    narrator "[line]"

    $ line = t("但他确信，不论明里暗里，眼下伫立在他身前的两位圣人定不单单在宣扬自己的教义，此中当还有别的深意……", "Yet he knew, in his heart of hearts, that the two sages standing before him were not merely preaching their doctrines—there was a deeper meaning beneath it all.")
    narrator "[line]"

    # ========== 试玩版到此结束 ==========
    scene black with fade
    $ line = t("—— 试玩版到此结束 ——\n\n少年还未迎上「第二审：虚无」。\n\n感谢游玩。", "—— End of the Demo ——\n\nThe Second Trial: Emptiness still awaits him.\n\nThank you for playing.")
    centered "[line]"
    return
