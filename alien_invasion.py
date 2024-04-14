import pygame
import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from bullet import Bullets
from pygame.sprite import Group
from alien import Aliens


def run_game():
    # 初始化pygame
    pygame.init()
    # 设置窗口标题
    pygame.display.set_caption("哎哎哎")
    # 创建设置实例
    instance_settings = Settings()
    # 创建屏幕的对象
    screen = pygame.display.set_mode((instance_settings.screen_width, instance_settings.screen_height))
    # 创建飞船实例
    instance_ship = Ship(screen, instance_settings)

    # 创建子弹编组，也就是在屏幕上显示子弹的容器
    bullets = pygame.sprite.Group()

    # 创建外星人编组
    aliens = pygame.sprite.Group()
    # 创建外星人群
    gf.create_alien_fleet(instance_settings, screen, aliens, instance_ship)

    while True:
        # 获取在游戏过程中的操作
        gf.check_event(screen, instance_settings, instance_ship, bullets)
        # 更新飞船的连续移动
        instance_ship.update_ship()
        # 更新子弹位置以及屏幕中子弹数量
        gf.update_bullets(bullets)

        # 更新屏幕绘制内容
        gf.update_screen(screen, instance_settings, instance_ship, bullets, aliens)


run_game()
