import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, screen, instance_settings):
        super().__init__()
        # 初始化屏幕并获取屏幕的外接矩形
        self.screen = screen
        # 对象赋给一个变量这块有点奇葩，可能会报错
        self.instance_settings = instance_settings
        self.screen_rect = screen.get_rect()

        # 加载飞船图片并获取飞船外接矩形
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()

        # 将飞船绘制在屏幕底部中间
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 处理小数点的情况
        # 飞船外接x，y的小数部分暂时保存在自己定义的一个新属性中
        self.image_centerX = float(self.rect.centerx)
        self.image_centerY = float(self.rect.centery)

        # 连续移动标志,初始为false，根据检测的事件类型改变状态
        self.keep_moving_right = False
        self.keep_moving_left = False
        self.keep_moving_up = False
        self.keep_moving_down = False

    def center_ship(self):
        # 信息重置时 将飞船重置在屏幕中间;属性时对的 为什么没有生效呢
        self.center = self.screen_rect.centerx

    def update_ship(self):
        # 条件测试：右侧移动标志True且 右侧的边缘小于屏幕右侧边缘
        if self.keep_moving_right and self.rect.right < self.screen_rect.right:
            self.image_centerX += self.instance_settings.ship_speed

        # 条件测试：左侧移动标志True且 左侧的边缘大于0，0是x轴的原点
        elif self.keep_moving_left and self.rect.left >= 0:
            self.image_centerX -= self.instance_settings.ship_speed

        # 条件测试：向上移动标志为True且飞船边缘小于屏幕上边缘
        elif self.keep_moving_up and self.rect.top > self.screen_rect.top:
            self.image_centerY -= self.instance_settings.ship_speed

        # 条件测试： 向下移动标志为False且飞船边缘大于屏幕底部
        elif self.keep_moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.image_centerY += self.instance_settings.ship_speed

        # 根据self.center更新rect对象
        # 将暂时保存的x轴的值再重新赋给飞船的外接x，此处会有小数点取整的情况，对飞船显示来说问题不大
        self.rect.centerx = self.image_centerX
        self.rect.centery = self.image_centerY

    def blit_ship(self):
        self.screen.blit(self.image, self.rect)
