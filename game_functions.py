import pygame
import sys
from bullet import Bullets
from alien import Aliens


def check_event(screen, instance_settings, instance_ship, bullets):
    # 获取在游戏过程中的操作
    for event in pygame.event.get():
        # 条件测试 事件是点击屏幕x时退出
        if event.type == pygame.QUIT:
            sys.exit()
        # 条件测试 事件类型为摁下,check_event_keydown()
        elif event.type == pygame.KEYDOWN:
            check_event_keydown(event, screen, instance_settings, instance_ship, bullets)
        # 条件测试 事件类型为抬起，check_event_keyup()
        elif event.type == pygame.KEYUP:
            check_event_keyup(event, instance_ship)


def check_event_keydown(event, screen, instance_settings, instance_ship, bullets):
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
    elif event.key == pygame.K_F1:
        sys.exit()


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


def update_bullets(bullets):
    # 更新子弹移动
    bullets.update()
    # 对编组中的每个子弹精灵都进行一个绘制操作
    for bullet in bullets.copy():
        # 条件测试：删除在屏幕中消失的子弹
        if bullet.bullet_rect.centery <= 0:  # top 还是buttom,哪个也不是，哈哈哈
            bullets.remove(bullet)


def create_alien_fleet(instance_settings, screen, aliens, instance_ship):
    # 实例化外星人
    alien = Aliens(screen, instance_settings)
    # 通过实例获取一个外星人的宽和高
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = instance_ship.rect.height

    # 调用对应方法获得后续步骤所需的整数序列
    usable_number_alien_x = get_number_alien_row(instance_settings, alien_width)
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
        # 条件测试 返回值为True即外星人到达边缘，则下降并改变方向
        if alien.check_edges():
            change_alien_fleet_direction(aliens, instance_settings)
            break  # 如果没有break 如何看自己是不是进入了死循环？


def update_aliens(aliens, instance_settings):
    check_alien_fleet_edges(aliens, instance_settings)
    # 更新飞船位置;这个需要单独写个方法？至于吗？？？就不写！！！
    aliens.update()


def update_screen(screen, instance_settings, instance_ship, bullets, aliens):
    # 填充背景为图片
    screen.blit(instance_settings.bg_image, (0, 0))
    update_bullets(bullets)
    # 将子弹编组内的子弹在屏幕上进行绘制
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 将飞船绘制处理啊
    instance_ship.blit_ship()
    # # 更新飞船位置;这个需要单独写个方法？至于吗？？？就不写！！！
    # aliens.update()
    update_aliens(aliens, instance_settings)
    # 绘制编组中每个外星人
    aliens.draw(screen)

    # 将准备好的内容都显示出来
    pygame.display.flip()
