import pygame
import sys
from settings import Settings
from ship import Ship
import game_functions as gf
from bullet import Bullets
from pygame.sprite import Group
from alien import Aliens
from game_stats import GameStats
from button import Button
from scoreboard import  ScoreBoard


def run_game():
    # 初始化pygame
    pygame.init()
    # 设置窗口标题
    pygame.display.set_caption("Alien Invasion")
    # 创建设置实例
    instance_settings = Settings()
    # 创建屏幕的对象
    screen = pygame.display.set_mode((instance_settings.screen_width, instance_settings.screen_height))
    button_play = Button(instance_settings,screen, "Play")

    # 创建飞船实例
    instance_ship = Ship(screen, instance_settings)

    # 创建子弹编组，也就是在屏幕上显示子弹的容器
    bullets = pygame.sprite.Group()

    # 创建外星人编组
    aliens = pygame.sprite.Group()
    # 创建外星人群
    gf.create_alien_fleet(instance_settings, screen, aliens, instance_ship)

    # 创建一个游戏统计信息的实例
    stats = GameStats(instance_settings)
    score =ScoreBoard(screen, instance_settings, stats)


    while True:
        # 获取在游戏过程中的操作
        gf.check_event(screen, instance_settings, instance_ship, bullets, button_play, stats, aliens,score)

        if stats.game_active :
            # 更新飞船的连续移动
            instance_ship.update_ship()
            # 更新与子弹相关的内容，子弹移动、删除不在屏幕内的子弹、创建新的外星人群
            gf.update_bullets(instance_settings, screen, aliens, instance_ship, bullets,stats,score)
            # 更新与外星人相关内容，碰撞屏幕边缘改变移动方向、游戏次数、飞船与外星人碰撞重置部分信息
            gf.update_aliens(aliens, instance_settings, instance_ship, screen, bullets, stats,score)
            # 更新历史最高分
            gf.check_high_score(stats,score)
        # 更新屏幕绘制内容
        gf.update_screen(screen, instance_settings, instance_ship, bullets, aliens,stats,button_play,score)


run_game()
