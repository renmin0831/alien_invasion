import pygame.font


class Button:
    def __init__(self,instance_settings, screen, msg):
        # pygame.font.init()
        # 需要在屏幕上绘制出来，所以需要获取屏幕的矩形区域
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        # 设置字体的大小，文字颜色、背景色、位置
        self.button_width = 200
        self.button_height = 50
        self.button_bg_color = (0, 255, 0)

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("timesnewroman", 38)


        # 创建按钮的rect对象并剧中显示
        self.rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.rect.center = self.screen_rect.center

        # 将文字渲染成图像
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # 指定字体、字体颜色和按钮背景颜色,将文字渲染成图像
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_bg_color)

        # 获取字体的外接矩形并设置在按钮中间
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def button_blit(self):
        #填充按钮区域的颜色
        self.screen.fill(self.button_bg_color, self.rect)
        #将渲染的文字在屏幕中绘制出来
        self.screen.blit(self.msg_image, self.msg_image_rect)
