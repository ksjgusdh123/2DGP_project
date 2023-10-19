from pico2d import *

sonic_run = [7, 31, 56, 82, 105, 105, 130, 154, 180, 180]
sonic_jump = [6, 34, 55, 84, 109, 137, 165, 193, 219, 246]
sonic_jump_w = [21, 19, 24, 19, 25, 25, 23, 24, 24, 26]

tails_run = [79, 126, 174, 174, 222, 222, 271, 271, 319, 319]
tails_jump = [104, 223, 258, 298, 258, 223, 184, 151, 104, 104]
tails_jump_w = [32, 25, 30, 30, 30, 25, 24, 25, 32, 32]

shadow_run = [6, 6, 33, 33, 65, 65, 95, 117, 152, 152]
shadow_run_w = [26, 26, 27, 27, 23, 23, 20, 31, 24, 24]
shadow_jump = [146, 169, 169, 195, 195, 84, 84, 114, 114, 114]
shadow_jump_w = [19, 25, 25, 27, 27, 27, 27, 27, 27, 27]

ech_run =[4, 38, 76, 114, 153, 185, 185, 219, 260, 260]
ech_run_w =[32, 37, 38, 38, 30, 30, 30, 37, 38, 38]
ech_jump =[301, 301, 330, 363, 363, 397, 397, 219, 219, 260]
ech_jump_w =[27, 27, 31, 32, 32, 36, 36, 37, 37, 38]

class AI:
    ai_num = 0

    def __init__(self, player):
        if AI.ai_num == 0:
            self.image = load_image('sonic_animation.png')
        elif AI.ai_num == 1:
            self.image = load_image('tails.png')
        elif AI.ai_num == 2:
            self.image = load_image('shadow.png')
        elif AI.ai_num == 3:
            self.image = load_image('echidna.png')
        AI.ai_num += 1
        self.ch_id = AI.ai_num - 1
        self.frame = 0
        self.x, self.y = 100, 320 - self.ch_id * 60
        # self.speed = 5 + self.ch_id * 3
        self.speed = 5
        self.exceed_point = 950
        self.player = player
        self.jump = False
        self.time = get_time()
        self.finish = False

        pass

    def draw(self):
        self.draw_character()

    def draw_character(self):
        if self.ch_id == 0:
            if self.player.start == False:
                self.image.clip_draw(self.frame // 2 * 22 + 5, 249, 18, 30, self.x - self.player.camera_x, self.y, 50,
                                     100)
            else:
                if self.jump:
                    self.image.clip_draw(sonic_jump[self.frame], 215, sonic_jump_w[self.frame], 30,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(sonic_run[self.frame], 149, 23, 27, self.x - self.player.camera_x, self.y, 50,
                                         100)

        elif self.ch_id == 1:
            if self.player.start == False:
                self.image.clip_draw(self.frame // 2 * 32 + 107, 960, 21, 35, self.x - self.player.camera_x, self.y, 50,
                                     100)
            else:
                if self.jump:
                    self.image.clip_draw(tails_jump[self.frame], 736, tails_jump_w[self.frame], 32,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(tails_run[self.frame], 784, 36, 35, self.x - self.player.camera_x, self.y, 50,
                                         100)

        elif self.ch_id == 2:
            if self.player.start == False:
                self.image.clip_draw(self.frame // 2 * 26 + 6, 467, 23, 33, self.x - self.player.camera_x, self.y, 50,
                                     100)
            else:
                if self.jump:
                    self.image.clip_draw(shadow_jump[self.frame], 317, shadow_jump_w[self.frame], 39,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(shadow_run[self.frame], 431, shadow_run_w[self.frame], 32,
                                         self.x - self.player.camera_x, self.y, 50, 100)

        if self.ch_id == 3:
            if self.player.start == False:
                self.image.clip_draw(self.frame // 2 * 31 + 117, 262, 29, 42, self.x - self.player.camera_x, self.y, 50,
                                     100)
            else:
                if self.jump:
                    self.image.clip_draw(ech_jump[self.frame], 214, ech_jump_w[self.frame], 45,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(ech_run[self.frame], 218, ech_run_w[self.frame], 40, self.x - self.player.camera_x, self.y, 50,
                                         100)

    def update(self):
        # 게임 시작 시 sonic
        if self.player.start:
            if self.jump:
                self.x += 10
            else:
                self.x += self.speed
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

        if self.ch_id == 1 and not self.player.start:
            self.frame = (self.frame + 1) % 14
        else:
            self.frame = (self.frame + 1) % 10


        if self.x >= 5000 and self.finish == False:
            self.finish = True
            print(get_time() - self.time)
