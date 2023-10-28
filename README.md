# 游戏：外星人入侵
---------------
## 语言：python
* 使用 ___ pygame第三方库 ___ 进行开发  
    * 在运行该项目之前请确保您安装了这样的库  
---------------
## 游戏规则
* 玩家通过左右和空格控制底部的飞船移动和射击  
- 外星人从顶部向下移动，并随着波次速度提高  
* 当外星人撞到玩家飞船或者到达屏幕底部，玩家则会损失一艘飞船  
- 玩家一共有三艘飞船，全部损失则游戏失败  
---------------
## 项目组成
1. 主文件及其调用文件
    * [alien_invasion.py](/Alion_invasion/alien_invasion.py)
        1. setting.py
            * 提供游戏设置
        2. ship.py
            * 创建飞船
        3. bullet.py
            * 提供子弹
        4. alien.py
            * 提供外星人
        5. game_stats.py
            * 保存一些游戏统计信息
2. 副文件及其作用
    1. [settings.py](/Alion_invasion/settings.py)
        * 储存游戏里的各种设置
    2. [ship.py](/Alion_invasion/ship.py)
        - 创建飞船
    3. [bullet.py](/Alion_invasion/bullet.py)
        * 提供子弹
    4. [alien.py](/Alion_invasion/alien.py)
        * 提供外星人
    5. [game_stats.py](/Alion_invasion/game_stats.py)
        * 储存游戏统计信息
### 杂项  
* 本项目由python编写  
- 一个简单的开飞船打外星人的小游戏  
* 当前已经较为完善