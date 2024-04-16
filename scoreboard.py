import pygame.font
from ship import Ship


class ScoreBoard:
    def __init__(self, screen, instance_settings, stats):
        # 初始化屏幕所需信息
        self.screen = screen
        self.instance_settings = instance_settings
        self.instance_settings_rect = self.screen.get_rect()
        self.stats = stats

        # 设置字体的颜色、字体、字体大小
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("timesnewroman", 35)

        # 把文字渲染成图像；分数、历史高分、等级、代表游戏次数的飞船
        self.prep_score()
        self.prep_high_score()
        self.prep_game_level()
        self.prep_ships_life()

    def prep_score(self):
        # 将分数转化为字符串并格式化
        rounded_score = int(round(self.stats.score, -1))
        str_score = " {:,}".format(rounded_score)
        # 指定字体、字体颜色和背景颜色,将文字渲染成图像
        self.score_image = self.font.render(str_score, True, (255, 255, 255))
        # 获取外接矩形
        self.score_rect = self.score_image.get_rect()
        # 将分数显示在指定位置
        self.score_rect.right = self.instance_settings_rect.right - 20
        self.score_rect.top = self.instance_settings_rect.top + 20

    def prep_high_score(self):
        # 将分数转化为字符串并格式化
        rounded_high_score = int(round(self.stats.high_score, -1))
        str_high_score = "{:,}".format(rounded_high_score)
        # 指定字体、字体颜色和背景颜色,将文字渲染成图像
        self.high_score_image = self.font.render(str_high_score, True, (255, 255, 255))
        # 获取外接矩形
        self.high_score_rect = self.high_score_image.get_rect()
        # 将分数显示在指定位置
        self.high_score_rect.centerx = self.instance_settings_rect.centerx
        self.high_score_rect.top = self.instance_settings_rect.top + 20

    def prep_game_level(self):
        # 渲染等级，在指定位置显示
        str_level = str(self.stats.level)
        self.level_image = self.font.render(str_level, True, (255, 255, 255))
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships_life(self):
        # 显示剩余可使用飞船个数
        # 创建一个可使用飞船组
        self.ship_lifetimes = pygame.sprite.Group()
        for ship_number in range(self.stats.ships_life):
            # 创建一个ship实例
            ship = Ship(self.screen, self.instance_settings)
            # 将实例飞船放置到指定位置
            ship.rect.x = 10 + ship_number * ship.rect.width  # 位置可能有问题
            ship.rect.y = 10
            # 将实例飞船添加到可使用飞船组
            self.ship_lifetimes.add(ship)

    def score_blit(self):
        # 将渲染的文字显示出来；分数、历史高分、等级、飞船代表的可用次数
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ship_lifetimes.draw(self.screen)
