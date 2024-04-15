import pygame.font


class ScoreBoard:
    def __init__(self, screen, instance_settings, stats):
        # 初始化屏幕所需信息
        self.screen = screen
        self.instance_settings_rect = self.screen.get_rect()
        self.instance_settings = instance_settings
        self.stats_score = stats

        # 设置字体的颜色、字体、字体大小
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("timesnewroman", 35)

        # 把文字渲染成图像
        self.prep_score()

    def prep_score(self):
        # 将分数转化为字符串
        str_score = str(self.stats_score.score)
        # 指定字体、字体颜色和背景颜色,将文字渲染成图像
        self.score_image = self.font.render(str_score, True, self.text_color, self.instance_settings.bg_color)

        # 获取外接矩形
        self.score_rect = self.score_image.get_rect()

        # 将分数显示在指定位置
        self.score_rect.right = self.instance_settings_rect.right - 20
        self.score_rect.top = self.instance_settings_rect.top + 70

    def score_blit(self):
        # 将渲染的文字显示出来
        self.screen.blit(self.score_image, self.score_rect)
