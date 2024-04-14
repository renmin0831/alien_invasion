import pygame.image
from pygame.sprite import Sprite


class Bullets(Sprite):
    def __init__(self, screen, instance_settings, instance_ship):
        # 继承pygame下的精灵类
        super().__init__()

        # 初始化屏幕
        self.screen = screen
        # 初始化子弹属性，方便bullet模块使用，不用频繁访问settings模块
        self.bullet_color = instance_settings.bullet_color
        self.bullet_speed = instance_settings.bullet_speed

        # 在屏幕的右上角创建子弹
        self.bullet_rect = pygame.Rect(0, 0, instance_settings.bullet_width, instance_settings.bullet_height)

        # 将子弹设置在飞船的位置，与飞船xy轴相同
        self.bullet_rect.centerx = instance_ship.rect.centerx
        self.bullet_rect.centery = instance_ship.rect.top

        # 处理子弹移动的小数问题
        self.y = float(self.bullet_rect.centery)

    def update(self):
        # 子弹向上移动
        self.y -= self.bullet_speed
        # 将临时属性再赋值给原属性
        self.bullet_rect.centery = self.y

    def draw_bullet(self):
        # 将子弹绘制出来
        pygame.draw.rect(self.screen, self.bullet_color, self.bullet_rect)
