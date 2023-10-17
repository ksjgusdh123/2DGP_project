from pico2d import *

sonic_run = [7, 31, 56, 82, 105, 130, 154, 180]
sonic_slip = [4, 68, 95, 35]
sonic_jump = [6, 34, 55, 84, 109, 137, 165, 193, 219, 246]
sonic_jump_w = [21, 19, 24, 19, 25, 25, 23, 24, 24, 26]

class AI:
    def __init__(self, player):
        self.image = load_image('sonic_animation.png')
        self.frame = 0
        self.x, self.y = 100, 200
        self.exceed_point = 950
        self.player = player
        pass
    def draw(self):
        if self.player.start == False:
            self.image.clip_draw(self.frame // 2 * 22 + 5, 249, 18, 30, self.x - self.player.camera_x, self.y, 50, 100)
        else:
            self.image.clip_draw(sonic_run[self.frame], 149, 23, 27, self.x - self.player.camera_x, self.y, 50, 100)

        pass
    def update(self):
        # 게임 시작 시
        if self.player.start:
            self.x += 10
            self.frame = (self.frame + 1) % 8
        else:
            self.frame = (self.frame + 1) % 10
