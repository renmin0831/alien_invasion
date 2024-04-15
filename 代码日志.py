"""
1.创建pygame窗口以及响应用户输入
    使用pygame库时，总忘记需要初始化 --记住了
    set_mode()长宽时一个元组，总是少写括号 --记住了

    解决：窗口绘制方法不记得了， fill() 和 flip()方法
    fill()接受一个RGB的颜色填充，
    flip()屏幕绘制，在循环末尾使用，随着每次循环，将屏幕擦除重新绘制，
    updat()与filp()差不多，区别是update只绘制指定的位置，不是整个屏幕重新绘制

2.设置背景颜色
    拓展：想把背景替换成图片的，替换失败
        1.加载背景图片资源
        2.使用pygame.transform.scale()方法，
            self.bg_image = pygame.image.load("images/bg.png")
            self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        3.使用该方法后，绘制方法也需要使用 screen.blit()；blit()参与图像绘制，flip()参与屏幕更新
            screen.blit(instance_settings.bg_image, (0, 0))
3.创建设置类
    添加设置model，导入到alien_invasion使用时，忘记创建屏幕对象，--看不懂了

4.添加飞船图像
    写完飞船相关代码，想要在本模块下调试，不会
    飞船设x，y坐标错了，一开始设置在了0，0 的位置，是因为blit()方法中参数传错了，传了个屏幕坐标，应是飞船图和飞船坐标

    解决1：忘记了飞船模块的结构
        1.初始化屏幕并获取屏幕的外接矩形
        2.加载飞船资源并获取飞船资源的外接矩形
        3.将飞船设置在屏幕的底部中间
        4.绘制飞船
    解决2：blit()方法不记得了
        需要绘制surface对象就使用blit(),参数是资源，资源坐标元组

5.重构game_function模块
    没有模块 只有方法的导入及使用，不熟练--记住了
    第一次重构：将获取游戏过程中的操作移到gf中，创建个新方法check_event。简化循环中的内容
    第二次重构：将屏幕需要重新绘制的内容移到gf中，创建个新方法update_screen。简化循环中的内容
    第三次重构：将控制左右连续移动分别用2个方法实现,通过监测事件类型调用对应方法

6. 进一步简化run_game，绘制方法可以放入game_function中
    解决1：那些内容需要移动到screen_update中
        见5重构部分，只说明screen_update中的内容，应该就是都是图像绘制的内容都在这个方法里
    解决2：ship参数是个啥
        # 这块的参数与screen_update中的参数名不一样，目前看是位置参数，位置不一样会报错，一样正常运行
        gf.screen_update(screen, instance_setting.bg_color, instance_ship)

        有些内置方法对参数位置有要求，用的时候注意下。自己写的方法本身参数个数和位置在调用的时候一起粘过去就能解决这个问题。因为是调用的方法，参数一定是和
    被调用的方法参数保持一致，要不执行被调用的方法时内部逻辑会报错。

7.响应按键，让飞船移动，且连续移动
    bug记录：记录的什么乱七八糟的，看都看不懂
        响应事件有bug，需要触发的不会调试pygame.KEYDOWN 写成了K_DOWN
        设置连续移动的时候 KEYUP 写错了导致一直往右侧移动，抬起也不停止
        check event 老写错 啊西巴 抬起也是K_RIGHT 没K_UP

    解决1：让飞船左右移动的步骤是啥来的？--看了一眼书就想起来了
        检查事件是keydown  不是K_DOWN啊啊啊啊！
        1.先做右侧移动，移动1个像素位置，更新screen_updata查看结果对不对
        2.使用连续移动标志让飞船可右侧连续移动
        3.再以同样的方法修改左侧移动，并可连续从左侧移动
        4.设置左右边界
        6.重构下gf中事件的检测，抬起，摁下和事件获取要分别用方法实现
    解决2：飞船不按照要求左右移动的问题
        event.type 是监测事件类型
            type：KEYDOWN、KEYUP
        event.key 是检测摁下的“左右”键
            key：K_RIGHT、K_LEFT
    解决3：ship_rect.center与ship_rect.centerx的区别是啥？
        center：获取矩形中心点的坐标时可用，返回一个包含xy坐标的元组
        centerx：获取矩形的中心点x坐标时可用，返回x坐标属性

    解决4：怎么将活动标志和飞船连续移动关联起来呢？
        新增一个update方法，将移动的速度和移动边界通过该方法进行更新，别忘记需要在循环中调用该方法
        具体步骤见解决1

    解决5：小数点没有设置，但是也不影响移动，怎么触发小数的情况导致的bug呢
        以0.5为例，x轴+0.5像素的时候会向上取整(1)， -0.5像素的时候会向下取整(0)，无法向左侧移动
        1，将飞船的外接x属性转换为float型，保存在自定义的新属性中
        2.在update_ship()方法中 计算飞船位置时使用
        3.不再计算时在将飞船的临时x轴属性再赋给原属性，如果数值有小数会存在取整的情况

    拓展：将飞船除了左右移动外，可以上下移动
        y轴和x轴移动其实是一样的，需要搞清楚坐标系的原点在哪里
        pygame的原点坐标系在左上角(0,0)
        左上角为原点坐标系的情况下：y轴的正方向是向下的；计算机图形学使用；根据设备屏幕显示一致
            y轴向上 为 top，值-1
            y轴向下，为bottom，值+1
        左下角为原点坐标系的情况下： 数学绘图使用
            y轴向上 为 bottom，值+1
            y轴向下，top，值-1

8.添加子弹设置、创建子弹类
    bug记录
        不会。。。。。。非常不会，完全没思路--已解决
        继承格式写错了，super().__init__()   super.__init__() 也没写继承谁-已解决
        忘记写子弹向上的方法了，
        删除已消失的子弹咋写

    解决1：blit()绘制方法与draw()绘制方法的区别
        pygame.Rect()方法
            创建矩形的方法，需要提供四个值，（x坐标，y坐标，矩形长，矩形宽）

        blit()绘制方法与draw()绘制方法的区别
            blit()绘制方法是一个surface对象绘制在另外一个surface对象上时使用;surface.blit(对象，位置)
                self.screen.blit(self.ship_image, self.ship_image_rect)
            pygame.draw.rect(surface对象，颜色，绘制的线条)用于在surface对象上绘制各种线条，且不需要加载图像
                pygame.draw.rect(self.screen, self.bullet_color, self.bullet_rect)

    解决2：子弹在飞机上层还是下层，是在中心对齐还是顶部对齐
        self.bullet_rect.centery = instance_ship.ship_image_rect.top 子弹在飞机顶部
        self.bullet_rect.centery = instance_ship.ship_image_rect.centery子弹在飞机身上

    解决3：子弹编组 完全没思路
        步骤
            1.创建编组
            2.更新check_event_keydown 创建新的子弹实例并加入到编组中，因为编组是指屏幕内显示的子弹
            3.重绘编组中的子弹
            4.删除消失的子弹，更新时要注意先删除后添加
            5。屏幕中的子弹限制

    解决4：子弹发射不移动使什么鬼，应该从哪里开始分析 ？ 原因使 bullet_update 没生效，改成update就生效了？？为什么呢？
        已经无法知道具体原因，大致猜测是因为有2点，1在检查check_event_down()没有创建新的子弹，并且，没有对子弹编组和子弹实例关联导致
        2.在子弹绘制的时候没有修改绘制方法，应通过for循环对子弹列表进行重新绘制。

    解决5：重绘精灵的方法不懂 bullets.sprites()
        xxx.sprites()是pygame.sprite.Grop的一个方法，返回一个包含xx精灵对象的列表，该列表通常在循环中对每个精灵对象进行操作

9.编写外星人类
    bug记录
    重构create_alien_fleet，分成get_number_alien和create_alien()是怎么能想不清楚怎么重构呢！！！
    添加外星人的一行多少个外星人和一共多少行
    创建外星人这块gf文件拆分成了好多个方法，不太理解里面参数传递的过程--一解决，上面有关于参数传递
    有点理解不断重构了，也有点理解为啥当初写的时候参数一直搞不明白的，到底是位置还是关键

    解决1： range(usable_space_x) 与 len(usable_space_x)的区别
            len()函数用于返回一个序列（如列表、元组、字符串等）的长度或元素个数
            range()函数用于生成一个整数序列，通常用于循环中

    解决2 为什么使用aliens(screen),不再使用外星人模块中的blit()绘制方法
        继承了Sprite类，所以需要使用该类下的绘制方法对精灵对象进行统一管理

    解决3：创建一群外星人的步骤
        计算出一行能显示多少个外星人并正确显示出来
            # 计算每个外星人的x坐标
            # 计算当前外星人在当前行的位置
        计算出屏幕能显示多少行外星人并正确显示出来

    解决4，精灵实例和精灵编组如何进行关联；实例和编组需要关联，要不没法使用
        在game_functions模块下，编写一个方法用于创建 一个外星人，并将其加入到精灵列表中，后续访问精灵列表进行操作就可以了
        子弹实例和子弹编组关联方法同外星人精灵，创建子弹实例并加入到子弹编组中


    解决5：
        //2 与不//2 的区别
        self.alien_image_rect.centerx = self.alien_image_rect.width //2
        self.alien_image_rect.centery = self.alien_image_rect.height //2

        取整的话就是在


    解决6：将首个外星人设置在屏幕左上角，为什么会是外星人本身的宽高；为什么飞船就没有设置呢？与碰撞检测有关系吗？
            这个问题有待解决


    解决7：像子弹、外星人需要继承精灵类呢；总是没有继承精灵哎
        pygame.sprite.Sprite类，封装了一系列方法进行统一管理精灵实例，比如添加、删除、碰撞以及在屏幕上绘图、更新等。
        如果要是自己写方法去管理对象，1个是代码复杂度上升，在游戏方面对象也不仅仅是几个，而是几百几千甚至更多，在对象的管理上也增加了难度。



    解决8：获取图像矩形，赋值给rect对rect属性初始化；没有理解的情况下导致各种问题
        例如：AttributeError: 'Aliens' object has no attribute 'image'

        Aliens类继承了pygame.sprite.Sprite类，在初始化该基类的时候也要对该类下的rect属性进行初始化，并与子类的属性进行关联，方便后续使用
        图像矩形时的属性访问。上述bug就是因为在初始化时没有对rect和image属性进行初始化，在后续访问图像矩形的属性时没有对应的属性导致报错。
        用别人写的方法 就需要遵从规定的写法。



    解决9：在计算容纳多少行是，由于对公式的不理解，应取alien_height取成了alien_width;行的参数传错了
        1。先计算出上下可以用空间，需要去掉外星人和外星人上面的空白高度，以及飞船占用的高度
        2.使用剩余空间除以摆放一个飞船所需的高度，就得出能放多少行



    解决10：这段代码 怎么都理解不了，应该是外星人创建那就没明白每段代码的意思
            def create_alien(instance_setting, screen, aliens, alien_number):
            # 创建一个外星人实例，其中包含
            alien = Alien(instance_setting, screen)
            # 将实例中外星人的宽度赋给当前变量alien_width
            alien_width = alien.rect.width  #获取实例外星人的宽度
            alien.x = alien_width + 2 * alien_width * alien_number  # 将每个外星人向右侧移动一个位置，设置外星人x坐标
            alien.rect.x = alien.x    #懂这个是啥意思。。赋值给外星人实例吗？？？？
            aliens.add(alien)
        self.rect.x = self.x  啥意思？？？

18. 让外星人移动
    让外星人向右移动
    检测外星人是否撞到了屏幕边缘，撞到边缘向下移动并改变方向
    break # 如果没有break 如何看自己是不是进入了死循环？

19    游戏碰撞是指 游戏重叠在一起 sprite.groupcollide()
    为社么要在bullets_update 里判断屏幕是否还有外星人？？

20 检测外星人的碰撞
    pygame.sprite.groupcollide 是 Pygame 中用于检测精灵组之间碰撞的方法。
    它用于检测一个精灵组中的精灵是否与另一个精灵组中的精灵发生了碰撞，并将碰撞的结果以字典的形式返回。
    pygame.sprite.groupcollide(group1, group2, dokill1, dokill2, collided=None) -> dict
        group1: 第一个精灵组。
        group2: 第二个精灵组。
        dokill1: 如果为 True，则 group1 中发生碰撞的精灵会被删除。
        dokill2: 如果为 True，则 group2 中发生碰撞的精灵会被删除。
        collided: 用于指定一个碰撞检测函数，可以自定义碰撞的规则。
                如果不指定，则使用默认的碰撞检测规则，即两个精灵的 rect 属性之间的碰撞。

    检测：外星人和子弹碰撞、外星人和飞船碰撞
        pygame.sprite.groupcollide(sprite1,sprite2,True,True)
        pygame.sprite.spritecollideany(sprite, group, collided = None)三个参数：一个精灵，一个编组，默认使用精灵对象的rect属性判断碰撞

21 创建存储游戏统计信息
    想一下 创建的存储游戏统计信息，都要存储哪些信息呢
        游戏次数
        历史最高分
        本次游戏分数
        关卡数

    目标是3此机会，目前0 也能继续游戏，需要处理下0 的情况
    调用方法在init中初始化，和直接在init中初始化的区别是啥？
    给自己坑了 飞船在碰撞到外星人后 应该是在底部中间重置，但是没有，应该是参数传递错误

    gf里那么多方法 尤其是update的 我都已经不记得具体是要干啥的了

22 设置游戏结束的相关信息以及运行那部分内容
---------------------------------------------------------------------------------
23.添加play按钮
24创建button类
    想一想button类应该包含什么属性
    pygame中没有内置的创建按钮的方法， 创建带标签的实心矩形
    pygame.font.SysFont()s 是什么方法
    初始化的时候为什么没有setting
    self.font.render(msg, True, self.button_color, self.text_color)

    创建好button类后运行，屏幕中间没有出现play按钮；因为self.game_active = True
添加check_play_button
    pygame.mouse.get_pos()
处理游戏结束时的点击play按钮
    有些方法需要在不同的文件中重新调用哎。。。
    有个bug 飞船在重新开始后没有返回指定位置哎，，那为啥不报错，

将play按钮切换到非活动状态
    点击后再次点击相同区域,像不像测试中的测试点呀

隐藏光标   pygame.mouse.set_visible(False)
显示光标

设置速度等级并重置速度

25 记分
显示得分
    又一次不记得这个玩意
    是他是他就是他 self.font.render(score_str, True, self.text_color, self.instance_setting.bg_color)
创建记分牌
    self.score_image = self.font.render(score_str, True, self.text_color, self.instance_setting.bg_color)
    TypeError: text must be a unicode or bytes
    文字渲染 还是 图片渲染  搞不懂方法咋用的
    咦。。。。。。电脑好卡

外星人被消灭时更新得分
    将消灭的每个外星人的点数都计入得分
    处理 在一次循环中如果有两颗子弹射中了外星人，或因子弹宽而色号中更多外星人，的得分 像不像测试里的bug
    collisions 我什么时候把它设置成了字典了？好像没有哎
将分数处理成千分位
  score_str = "{:,}".format(rounded_score) 字符串格式设置指令，将数值转换为字符串时在其中放入逗号

处理最高得分
    最高得分的初始化位置，像不像每次测试最高得分会不会倍重置的情况
    添加新方法时，不知道要在哪些方法里添加相应的修改
显示等级


拓展：
    1.修改背景图为动态的
    2.修改外星人为动态的
    3.子弹和外星人发生碰撞后要有碰撞效果
    4.飞船尾部要有喷气的动态效果
    5.刷新外星人时，需要从上往下，显示当前关卡数，完成刷新前不允许开火











"""
