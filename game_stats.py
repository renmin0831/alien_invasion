class GameStats:
    def __init__(self, instance_settings):
        # 存储不变的信息
        # 初始化统计信息
        self.instance_settings = instance_settings
        self.reset_stats()

    def reset_stats(self):
        # 存储可变的信息
        # 初始化可变信息
        self.ships_life = self.instance_settings.bullet_limit
