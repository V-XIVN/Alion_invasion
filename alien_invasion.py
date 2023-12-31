import sys

import pygame

from time import sleep

from game_stats import GameStats

from settings import Settings

from ship import Ship

from bullet import Bullet

from alien import Alien

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

        # 创建一个用于储存游戏统计信息的实例
        self.stats = GameStats(self)

        # 创建一艘飞船
        self.ship = Ship(self)

        # 创建一个用于储存子弹的编组
        self.bullets = pygame.sprite.Group()

        # 创建一个外星人编组
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 游戏启动后处于活动状态
        self.game_active = True


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self._update_screen()

            if self.game_active:
                self.ship.update()
                self._update_aliens()
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

    def _ship_hit(self):
        """相应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将ships_left减一
            self.stats.ships_left -= 1

            # 清空外星人的列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()

            # 创建一个新的外形人舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False

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

        self._check_bullet_alien_collisions()

        if not self.aliens:
            # 删除现有的子弹并创建一个新的外星人舰队
            self.bullets.empty()
            self._create_fleet()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)            

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘，并更新整个外星人舰队的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()


    def _create_fleet(self):
        """创建一个外星人舰队"""
        # 创建一个外星人, 再不断添加，直到没有空间容纳外星人为止
        # 外星人的间距为外星人的宽度及其对应的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        # 填充直到没有空间容纳新的外星人
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - alien_width):
                self._create_alien(current_x, current_y)
                # 间距为外星人宽度
                current_x += 2 * alien_width

            # 添加一行外星人之后，重置x值并且递增y值
            current_x = alien_width
            current_y += 2 * alien_height
        
    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行列中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _check_aliens_bottom(self):
        """检测是否有外星人到达了屏幕的下边缘"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break


    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变他们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 将背景色填充在屏幕上
        self.screen.fill(self.settings.bg_color)
        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 绘制飞船
        self.ship.blitme()
        # 绘制外星人
        self.aliens.draw(self.screen)
        # 不断更新屏幕内容
        pygame.display.flip()

if __name__ == "__main__":
    # 创建游戏并开始游戏
    ai = AlienInvasion()
    ai.run_game()