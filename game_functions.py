import pygame
import sys
from bullet import Bullets
from alien import Aliens
from time import sleep



def check_event(screen, instance_settings, instance_ship, bullets, button_play, stats, aliens, score):
    # 获取在游戏过程中的操作
    for event in pygame.event.get():
        # 条件测试 事件是点击屏幕x时退出
        if event.type == pygame.QUIT:
            sys.exit()
        # 条件测试 事件类型为摁下,check_event_keydown()
        elif event.type == pygame.KEYDOWN:
            check_event_keydown(event, screen, instance_settings, instance_ship, bullets, stats, aliens, score)
        # 条件测试 事件类型为抬起，check_event_keyup()
        elif event.type == pygame.KEYUP:
            check_event_keyup(event, instance_ship)
        # 条件测试 事件类型为鼠标点play按钮，返回play击坐标
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # 调用函数检查是否可以重新开始游戏，并重置部分游戏信息
            check_play_button_down(button_play, mouse_x, mouse_y, stats, aliens, bullets, instance_settings, screen,
                                   instance_ship, score)


def check_play_button_down(button_play, mouse_x, mouse_y, stats, aliens, bullets, instance_settings, screen,
                           instance_ship, score):
    # 条件测试 判断鼠标点击的位置是否在按钮图像内
    click_button = button_play.rect.collidepoint(mouse_x, mouse_y)
    # 条件测试 点击play按钮 并且 活动为false
    if click_button and not stats.game_active:
        # 调用函数，重置部分游戏信息
        start_game(stats, bullets, aliens, instance_settings, screen, instance_ship, score)


def start_game(stats, bullets, aliens, instance_settings, screen, instance_ship, score):
    # 重置游戏信息
    stats.reset_stats()
    # 重置活动状态
    stats.game_active = True

    # 重新绘制 分数、历史高分、游戏等级、代表游戏次数的飞船
    score.prep_score()
    score.prep_high_score()
    score.prep_game_level()
    score.prep_ships_life()

    # 清空子弹和飞船编组
    bullets.empty()
    aliens.empty()

    # 创建新的外新人群
    create_alien_fleet(instance_settings, screen, aliens, instance_ship)

    # 当活动处于非活动状态时，隐藏光标
    pygame.mouse.set_visible(False)


def check_event_keydown(event, screen, instance_settings, instance_ship, bullets, stats, aliens, score):
    # 条件测试 事件类型为摁下右箭头，修改连续移动标志为True
    if event.key == pygame.K_RIGHT:
        instance_ship.keep_moving_right = True
    # 条件测试 事件类型为摁下左箭头，修改连续移动标志为True
    elif event.key == pygame.K_LEFT:
        instance_ship.keep_moving_left = True
    # 条件测试 事件类型为上箭头，修改连续移动标注为True
    elif event.key == pygame.K_UP:
        instance_ship.keep_moving_up = True
    # 条件测试 事件类型为下箭头，修改连续移动标注为True
    elif event.key == pygame.K_DOWN:
        instance_ship.keep_moving_down = True
    # 条件测试 事件类型为摁下space，发出子弹
    elif event.key == pygame.K_SPACE:
        fire_bullets(screen, instance_settings, instance_ship, bullets)
    # 条件测试 事件类型为F1时退出游戏
    elif event.key == pygame.K_F1:
        sys.exit()
    # 条件测试 事件类型为TAB键时视为点击play按钮，重置部分属性并开始游戏
    elif event.key == pygame.K_TAB:
        start_game(stats, bullets, aliens, instance_settings, screen, instance_ship, score)


def check_event_keyup(event, instance_ship):
    # 条件测试 事件类型为抬起右箭头，修改连续标志为False
    if event.key == pygame.K_RIGHT:
        instance_ship.keep_moving_right = False
    # 条件测试 事件类型为抬起左箭头，修改连续标志为False
    elif event.key == pygame.K_LEFT:
        instance_ship.keep_moving_left = False
    # 条件测试 事件类型为抬起上箭头，修改连续标志为False
    elif event.key == pygame.K_UP:
        instance_ship.keep_moving_up = False
    # 条件测试 事件类型为抬起下箭头，修改连续标志为False
    elif event.key == pygame.K_DOWN:
        instance_ship.keep_moving_down = False


def fire_bullets(screen, instance_settings, instance_ship, bullets):
    # 创建新子弹实例并加入到编组中；在此处子弹实例和子弹编组关联
    new_bullet = Bullets(screen, instance_settings, instance_ship)
    # 测试条件 只有当前屏幕中的子弹数量小于限制数量才能添加
    if len(bullets) < instance_settings.bullet_limit:
        bullets.add(new_bullet)


def check_bullet_alien_collision(instance_settings, screen, aliens, instance_ship, bullets, stats, score):
    # 规范写法，返回一个字典保存在collisions
    # 检测子弹和外星人精灵组，发生碰撞时都被删除
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # 遍历字典，取出被子弹消灭的外星人数量
        for aliens in collisions.values():
            # 计算得分
            stats.score += instance_settings.alien_point * len(aliens)
            print(f"当前分数：{stats.score}")
            # 在屏幕上重新绘制分数
            score.prep_score()
        # 检查历史最高分是否需要重新赋值
        check_high_score(stats, score)

    # 条件测试 判断aliens中是否有外星人精灵，没有则重新生成
    elif len(aliens) == 0:
        # 清空屏幕上显示的子弹
        bullets.empty()
        # 增加level等级并在屏幕上重新绘制
        stats.level += 1
        score.prep_game_level()
        # 创建外星人群
        create_alien_fleet(instance_settings, screen, aliens, instance_ship)
        # level增加后难度增加，增加外星人移动速度
        instance_settings.increase_speed()
        # level增加后，增加消灭每个外星人的得分
        instance_settings.increase_score()


def check_high_score(stats, score):
    # 条件测试 当局分数高于最高分时最高分被重新赋值并在屏幕上绘出
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()


def create_alien_fleet(instance_settings, screen, aliens, instance_ship):
    # 实例化外星人
    alien = Aliens(screen, instance_settings)
    # 通过实例获取一个外星人的宽和高
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    # 获取飞船高度
    ship_height = instance_ship.rect.height

    # 获得每行可容纳的外星人数量
    usable_number_alien_x = get_number_alien_row(instance_settings, alien_width)
    # 获得可容纳的多少行外星人
    usable_number_alien_y = get_number_alien_column(instance_settings, alien_height, ship_height)

    # 遍历每一行获得y坐标
    for number_alien_y in range(usable_number_alien_y):
        # 遍历每一列获得x坐标
        for number_alien_x in range(usable_number_alien_x):
            # 添加外星人实例到编组中
            create_alien(screen, instance_settings, alien_width, aliens, number_alien_x, number_alien_y)


def create_alien(screen, instance_settings, alien_width, aliens, number_alien_x, number_alien_y):
    # 实例化外星人
    alien = Aliens(screen, instance_settings)

    # 计算每个外星人的x坐标,在右下角的x坐标
    alien.x = alien_width + 2 * alien_width * number_alien_x
    # 将每个外星人的x坐标赋给原外星人的rect属性，外星人实例获得该属性值
    alien.rect.x = alien.x

    # 计算每个外星人的y坐标，右下角的y坐标
    alien.y = alien.rect.height + 2 * alien.rect.height * number_alien_y
    # 将每个外星人的y坐标赋给原外星人的rect属性，外星人获得该属性值
    alien.rect.y = alien.y

    # 将外星人实例添加到外星人编组中；此处关联了外星人示实例和外星人编组
    aliens.add(alien)


def get_number_alien_row(instance_settings, alien_width):
    # 计算出可容纳外星人的水平空间
    usable_space_x = instance_settings.screen_width - (2 * alien_width)
    # 计算出一行能容纳多少外星人;屏幕的宽度，一个外星人的宽度，外星人之间的间隔
    usable_number_alien_x = int(usable_space_x / (2 * alien_width))
    return usable_number_alien_x


def get_number_alien_column(instance_settings, alien_height, ship_height):
    # 计算出可容纳外星人的空间
    usable_space_y = (instance_settings.screen_height - (3 * alien_height)) - ship_height
    # 计算出可容纳多少行外星人
    usable_number_alien_y = int(usable_space_y / (2 * alien_height))
    return usable_number_alien_y


def change_alien_fleet_direction(aliens, instance_settings):
    # 将编组中的外星人向下移动指定像素，并改变方向
    for alien in aliens.sprites():
        alien.rect.y += instance_settings.alien_fleet_drop
    instance_settings.alien_fleet_direction *= -1


def check_alien_fleet_edges(aliens, instance_settings):
    # 遍历外星人编组，查找是否有外星人到了边缘，
    for alien in aliens.sprites():
        # 条件测试 返回值为True即外星人到达边缘，则下降并改变方向；alien类中的方法
        if alien.check_edges():
            change_alien_fleet_direction(aliens, instance_settings)
            break


def check_ships_life(stats, score):
    # 条件测试 当代表游戏次数的飞船数量大于0时，次数-1并重新绘制代表可游戏次数的飞船
    if stats.ships_life > 0:
        stats.ships_life -= 1
        score.prep_ships_life()
    else:
        # 否则 游戏状态修改为False
        stats.game_active = False
        # 显示光标
        pygame.mouse.set_visible(True)


def alien_ship_stats_reset(instance_settings, screen, aliens, instance_ship, bullets, stats, score):
    # 重置游戏部分信息
    # 检查飞船数量是否可以继续游戏
    check_ships_life(stats, score)
    # 清空外星人和子弹列表
    aliens.empty()
    bullets.empty()

    # 重置飞船位置以及飞船可用数量
    instance_ship.center_ship()  # 返回数据时对的，就是位置没动

    # 创建新的外星人编组
    create_alien_fleet(instance_settings, screen, aliens, instance_ship)
    score.prep_ships_life()
    # 重置游戏速度相关信息
    instance_settings.initialize_dynamic_settings()
    # # 重置当前游戏分数
    # stats.reset_stats()
    # 重新生成编组时需要强制等待x秒后显示
    sleep(3)


def check_aliens_screen_bottom_edges(instance_ship, aliens, instance_settings, screen, bullets, stats, score):
    # 检查外星人是否触碰到屏幕底部
    screen_rect = instance_ship.screen_rect
    # 遍历外星人组确定是否有外星人触碰到屏幕底部
    for alien in aliens.sprites():
        # 条件测试 外星人底部碰到了屏幕底部，重置部分属性，重新开始游戏
        if alien.rect.bottom >= screen_rect.bottom:
            alien_ship_stats_reset(instance_settings, screen, aliens, instance_ship, bullets, stats, score)
            break


def update_bullets(instance_settings, screen, aliens, instance_ship, bullets, stats, score):
    # 该方法更新与子弹相关的内容
    # 更新子弹移动 bullet类中自己写的方法
    bullets.update()

    # 对编组中的每个子弹精灵都进行一个绘制操作
    for bullet in bullets.copy():
        # 条件测试：删除在屏幕中消失的子弹;bottom
        if bullet.rect.centery <= 0:
            bullets.remove(bullet)

    # 调用方法生成新的外星人
    check_bullet_alien_collision(instance_settings, screen, aliens, instance_ship, bullets, stats, score)


def update_aliens(aliens, instance_settings, instance_ship, screen, bullets, stats, score):
    # 更新与外星人相关的内容
    # 如有外星人碰到屏幕边缘，向下移动并，改变移动方向
    check_alien_fleet_edges(aliens, instance_settings)
    # 改变移动方向；alien类中的方法
    aliens.update()

    # 遍历外星人编组，返回第一个与飞船发生碰撞的外星人
    if pygame.sprite.spritecollideany(instance_ship, aliens):
        # 发生碰撞后重置外星人、子弹、飞船
        alien_ship_stats_reset(instance_settings, screen, aliens, instance_ship, bullets, stats, score)
    # 如果有外星人到达低端，重置部分信息
    check_aliens_screen_bottom_edges(instance_ship, aliens, instance_settings, screen, bullets, stats, score)


def draw_bullet(bullets):
    # 将子弹编组内的子弹在屏幕上进行绘制
    for bullet in bullets.sprites():
        bullet.draw_bullet()


def update_screen(screen, instance_settings, instance_ship, bullets, aliens, stats, button_play, score):
    # 填充背景为图片
    screen.blit(instance_settings.bg_image, (0, 0))
    # 将子弹编组内的子弹在屏幕上进行绘制
    draw_bullet(bullets)
    # 绘制飞船
    instance_ship.blit_ship()
    # 绘制编组中每个外星人
    aliens.draw(screen)

    # 绘制分数
    score.score_blit()

    # 测试条件 游戏状态为False，重绘开始按钮
    if not stats.game_active:
        button_play.button_blit()

    # 将准备好的内容都显示出来
    pygame.display.flip()
