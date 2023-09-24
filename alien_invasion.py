import sys

import pygame

from settings import Settings

from ship import Ship

from bullet import Bullet

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化pygame设置
        pygame.init() 
        # 定义一个时钟
        self.clock = pygame.time.Clock()
        # 初始化设置
        self.settings = Settings()
        # 创建一个显示窗口，当前设置为1200*800像素
        # 赋值的右值是一个surface对象,他是一个pygame的对象
        # surface在每次循环时都会重绘窗口
        self.screen = pygame.display.set_mode((self.settings.screen_width ,self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        # 创建一艘飞船
        self.ship = Ship(self)

        # 创建一个用于储存子弹的编组
        self.bullets = pygame.sprite.Group()


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self._update_screen()
            self.ship.update()
            self._update_bullets()

            # 保证游戏所在的循环每秒运行165帧，等同于设置刷新率
            self.clock.tick(165)

    def _check_events(self):
        """响应按键和鼠标事件--- 以_开头的方法为私有方法"""
        for event in pygame.event.get():
            # 如果事件包含用户关闭游戏，则退出游戏
            if event.type == pygame.QUIT:
                sys.exit()
            # 如果是其他按键事件，触发有效的对应反应
            # 使用pygame提供的接口判断按键是否被按下
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

        
    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # 按q键退出游戏
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """更新子弹的位置，并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 将背景色填充在屏幕上
        self.screen.fill(self.settings.bg_color)
        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 绘制飞船
        self.ship.blitme()
        # 不断更新屏幕内容
        pygame.display.flip()

if __name__ == "__main__":
    # 创建游戏并开始游戏
    ai = AlienInvasion()
    ai.run_game()