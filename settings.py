import pygame


class Settings:
    def __init__(self):
        # 设置屏幕属性
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = 230, 230, 230  # RGB颜色
        self.bg_image = pygame.image.load("images/bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))

        # 设置飞船属性
        self.ship_speed = 10

        # 设置子弹属性
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 60)
        self.bullet_speed = 5
        self.bullet_limit = 3

        # 设置外星人属性
        self.alien_fleet_speed = 1
        # 1向右移动 -1向左移动
        self.alien_fleet_direction = 1
        # 触碰边缘后向下移动的像素
        self.alien_fleet_drop = 1
