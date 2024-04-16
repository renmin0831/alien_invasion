
import pygame


class Settings:
    def __init__(self):
        # 初始化屏幕上的属性
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = 230, 230, 230  # RGB颜色
        self.bg_image = pygame.image.load("images/bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))

        # 设置子弹属性 长、宽、颜色、在屏幕上可存在的数量
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (255, 255, 60)
        self.bullet_limit = 2
        # 每盘游戏可使用的小命
        self.ship_limit = 2
        # 触碰边缘后向下移动的像素
        self.alien_fleet_drop = 5
        # 设置难度，外星人移动速度增长倍数
        self.speed_up_scale = 1.5
        # 等级提升后分数增长倍数
        self.score_up_scale = 1.5
        # 每次开始游戏初始化的游戏信息，与stats游戏信息重置差不多思路
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # 消灭外星人得分
        self.alien_point = 1
        # 飞船速度
        self.ship_speed = 10
        # 子弹速度
        self.bullet_speed = 30
        # 外星人整体下移指定像素
        self.alien_fleet_speed = 7
        # 初始右移动；1向右移动 -1向左移动，值只能是正负1
        self.alien_fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_fleet_speed *= self.speed_up_scale

    def increase_score(self):
        # 得分存在小数时进行取整
        self.alien_point = int(self.alien_point * self.score_up_scale)
