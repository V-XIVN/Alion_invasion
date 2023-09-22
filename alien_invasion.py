import sys

import pygame

from settings import Settings

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化背景设置
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

        def run_game(self):
            """开始游戏的主循环"""
            while True:
                # 监听键盘和鼠标事件
                for event in pygame.event.get():
                    # 如果事件包含用户关闭游戏，则退出游戏
                    if event.type == pygame.QUIT:
                        sys.exit()

                # 将背景色填充在屏幕上
                self.screen.fill(self.settings.bg_color)
                
                # 不断更新屏幕内容
                pygame.display.flip()
                # 保证游戏所在的循环每秒运行165帧，等同于设置刷新率
                self.clock.tick(165)

if __name__ == "__main__":
    # 创建游戏并开始游戏
    ai = AlienInvasion()
    ai.eun_game()