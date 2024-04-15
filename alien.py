import pygame.image
from pygame.sprite import Sprite


class Aliens(Sprite):
    def __init__(self, screen, instance_settings):
        # 继承精灵类并初始化
        super().__init__()
        # 初始化屏幕属性
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.instance_settings = instance_settings

        # 加载外星人图片资源
        self.image = pygame.image.load("images/alien.png")
        # 获取图像矩形，赋值给rect对rect属性初始化；rect是基类的属性，表示精灵对象的矩形区域
        self.rect = self.image.get_rect()
        # 将首个外星人设置在屏幕左上角,默认位置(0,0)
        # 将外星人的中心点设置成自身的宽和高，中心点在右下角；这样做为了方便后续碰撞检测用的吗/(ㄒoㄒ)/~~
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 处理外星人x,y坐标的小数情况
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        # 测试条件 外星人图像超出右侧 则返回True，让调用该方法的方法通过测试条件，外星人整体下降并改变方向
        if self.rect.right >= self.screen_rect.right:
            return True
        # 测试条件 外星人图像超出左侧 则返回True，让调用该方法的方法通过测试条件，外星人整体下降并改变方向
        elif self.rect.left <= 0:
            return True

    def update(self):
        # 通过结果是正负数判断向左还是向右移动，当前是右侧
        self.x += (self.instance_settings.alien_fleet_speed * self.instance_settings.alien_fleet_direction)
        self.rect.x = self.x

    def blit_alien(self):
        # 在屏幕上绘制出外星人
        self.screen.blit(self.image, self.rect)
