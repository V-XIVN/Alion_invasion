import pygame

import os

class Ship:
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # 移动标志（飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False

        # 获取飞船图像的路径
        self.path = os.path.join(os.getcwd(), "Alion_invasion/images/ship.png")

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        
        # 使用一个额外的浮点数类型储存飞船的准确位置
        self.x = float(self.rect.x)
        
    def update(self):
        """根据移动标志调整飞船位置"""
        # 只有在飞船下一步行动仍能够位于屏幕内时才允许继续移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0 :
            self.x -= self.settings.ship_speed

        # 使用浮点数类型的x更新rect对象
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船放在屏幕底部的中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)