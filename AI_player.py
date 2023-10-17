from pico2d import *

sonic_run = [7, 31, 56, 82, 105, 105, 130, 154, 180, 180]
sonic_jump = [6, 34, 55, 84, 109, 137, 165, 193, 219, 246]
sonic_jump_w = [21, 19, 24, 19, 25, 25, 23, 24, 24, 26]

tails_run = [79, 126, 174, 174, 222, 222, 271, 271, 319, 319]
tails_jump = [104, 223, 258, 298, 258, 223, 184, 151, 104, 104]
tails_jump_w = [32, 25, 30, 30, 30, 25, 24, 25, 32, 32]

class AI:
    def __init__(self, player, num):
        if num == 0:
            self.image = load_image('sonic_animation.png')
        elif num == 1:
            self.image = load_image('tails.png')
        self.ch_id = num
        self.frame = 0
        self.x, self.y = 100, 200
        self.exceed_point = 950
        self.player = player
        self.jump = False
        pass
    def draw(self):
        self.draw_character()

    def draw_character(self):
        if self.ch_id == 0:
            if self.player.start == False:
                 self.image.clip_draw(self.frame // 2 * 22 + 5, 249, 18, 30, self.x - self.player.camera_x, self.y, 50, 100)
            else:
                if self.jump:
                     self.image.clip_draw(sonic_jump[self.frame], 215, sonic_jump_w[self.frame], 30,
                                   self.x - self.player.camera_x, self.y, 50, 100)
                else:
                     self.image.clip_draw(sonic_run[self.frame], 149, 23, 27, self.x - self.player.camera_x, self.y, 50, 100)

        elif self.ch_id == 1:
            if self.player.start == False:
                self.image.clip_draw(self.frame // 2 * 32 + 107, 960, 21, 35, self.x - self.player.camera_x, self.y, 50,
                                     100)
            else:
                if self.jump:
                    self.image.clip_draw(tails_jump[self.frame], 736, tails_jump_w[self.frame], 32,
                                      self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(tails_run[self.frame], 784, 36, 35, self.x - self.player.camera_x, self.y, 50, 100)

    def update(self):
        if self.ch_id == 0:
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
        elif self.ch_id == 1:
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

            else:
                self.frame = (self.frame + 1) % 14
# class AI:
#     def __init__(self, player):
#         self.image = load_image('sonic_animation.png')
#         self.frame = 0
#         self.x, self.y = 100, 200
#         self.exceed_point = 950
#         self.player = player
#         self.jump = False
#         pass
#     def draw(self):
#         if self.player.start == False:
#             self.image.clip_draw(self.frame // 2 * 22 + 5, 249, 18, 30, self.x - self.player.camera_x, self.y, 50, 100)
#         else:
#             if self.jump:
#                 self.image.clip_draw(sonic_jump[self.frame], 215, sonic_jump_w[self.frame], 30,
#                            self.x - self.player.camera_x, self.y, 50, 100)
#             else:
#                 self.image.clip_draw(sonic_run[self.frame], 149, 23, 27, self.x - self.player.camera_x, self.y, 50, 100)
#
#         pass
#     def update(self):
#         # 게임 시작 시
#         if self.player.start:
#             if self.jump:
#                 self.x += 10
#             else:
#                 self.x += 5
#             if self.jump == False and self.x >= self.exceed_point:
#                 self.jump = True
#                 self.frame = 0
#             elif self.jump and self.x - self.exceed_point < 50:
#                 self.y += 10
#             elif self.jump and self.x - self.exceed_point >= 100:
#                 self.jump = False
#                 self.frame = 0
#                 self.exceed_point += 500
#             elif self.jump and self.x - self.exceed_point > 50:
#                 self.y -= 10
#
#         self.frame = (self.frame + 1) % 10
