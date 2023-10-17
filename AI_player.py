from pico2d import *

sonic_run = [7, 31, 56, 82, 105, 105, 130, 154, 180, 180]
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
        self.jump = False
        pass
    def draw(self):
        if self.player.start == False:
            self.image.clip_draw(self.frame // 2 * 22 + 5, 249, 18, 30, self.x - self.player.camera_x, self.y, 50, 100)
        else:
            if self.jump:
                self.image.clip_draw(sonic_jump[self.frame], 215, sonic_jump_w[self.frame], 30,
                           self.x - self.player.camera_x, self.y, 50, 100)
            else:
                self.image.clip_draw(sonic_run[self.frame], 149, 23, 27, self.x - self.player.camera_x, self.y, 50, 100)

        pass
    def update(self):
        # 게임 시작 시
        if self.player.start:
            if self.jump:
                self.x += 10
            else:
                self.x += 5
            if self.jump == False and self.x >= self.exceed_point:
                self.jump = True
                self.frame = 0
            elif self.jump and self.x - self.exceed_point < 50:
                self.y += 10
            elif self.jump and self.x - self.exceed_point >= 100:
                self.jump = False
                self.frame = 0
                self.exceed_point += 500
            elif self.jump and self.x - self.exceed_point > 50:
                self.y -= 10

        self.frame = (self.frame + 1) % 10
