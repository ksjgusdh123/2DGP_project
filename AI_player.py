from pico2d import *

import game_framework
from character_sprite import *

PIXEL_PER_METER = 10 / 0.3
RUN_SPEED_KMPH = 20
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000 / 60
RUN_SPEED_MPS = RUN_SPEED_MPM / 60
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class AI:
    ai_num = 0
    num = -1

    def __init__(self, player):
        self.player = player

        if self.player.character_id == 0:
            if AI.ai_num == 0:
                AI.ai_num += 1
                self.image = load_image('image/tails.png')
            elif AI.ai_num == 2:
                self.image = load_image('image/shadow.png')
            elif AI.ai_num == 3:
                self.image = load_image('image/echidna.png')
        elif self.player.character_id == 1:
            if AI.ai_num == 0:
                self.image = load_image('image/sonic_animation.png')
            elif AI.ai_num == 1:
                AI.ai_num += 1
                self.image = load_image('image/shadow.png')
            elif AI.ai_num == 3:
                self.image = load_image('image/echidna.png')
        elif self.player.character_id == 2:
            if AI.ai_num == 0:
                self.image = load_image('image/sonic_animation.png')
            elif AI.ai_num == 1:
                self.image = load_image('image/tails.png')
            elif AI.ai_num == 2:
                AI.ai_num += 1
                self.image = load_image('image/echidna.png')
        elif self.player.character_id == 3:
            if AI.ai_num == 0:
                self.image = load_image('image/sonic_animation.png')
            elif AI.ai_num == 1:
                self.image = load_image('image/tails.png')
            elif AI.ai_num == 2:
                self.image = load_image('image/shadow.png')
        AI.ai_num += 1
        AI.num += 1
        self.ch_id = AI.ai_num - 1
        self.frame = 0
        self.x, self.y = 100, 320 - AI.num * 60
        # self.speed = 5 + self.ch_id * 3
        self.speed = 1
        self.exceed_point = 950
        self.jump = False
        self.time = get_time()
        self.finish = False
        self.mode = None

    def draw(self):
        self.draw_character()

    def draw_character(self):
        if self.ch_id == 0:
            if not self.player.start:
                self.image.clip_draw(int(self.frame) // 2 * 22 + 5, 249, 18, 30, self.x - self.player.camera_x, self.y, 50, 100)
            else:
                if self.jump:
                    self.image.clip_draw(sonic_jump[int(self.frame)], 215, sonic_jump_w[int(self.frame)], 30,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(sonic_run[int(self.frame)], 149, 23, 27, self.x - self.player.camera_x, self.y, 50, 100)

        elif self.ch_id == 1:
            if not self.player.start:
                self.image.clip_draw(int(self.frame) // 2 * 32 + 107, 960, 21, 35, self.x - self.player.camera_x, self.y, 50, 100)
            else:
                if self.jump:
                    self.image.clip_draw(tails_jump[int(self.frame)], 736, tails_jump_w[int(self.frame)], 32,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(tails_run[int(self.frame)], 784, 36, 35, self.x - self.player.camera_x, self.y, 50, 100)

        elif self.ch_id == 2:
            if not self.player.start:
                self.image.clip_draw(int(self.frame) // 2 * 26 + 6, 467, 23, 33, self.x - self.player.camera_x, self.y, 50, 100)
            else:
                if self.jump:
                    self.image.clip_draw(shadow_jump[int(self.frame)], 317, shadow_jump_w[int(self.frame)], 39,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(shadow_run[int(self.frame)], 431, shadow_run_w[int(self.frame)], 32,
                                         self.x - self.player.camera_x, self.y, 50, 100)

        if self.ch_id == 3:
            if not self.player.start:
                self.image.clip_draw(int(self.frame) // 2 * 31 + 117, 262, 29, 42, self.x - self.player.camera_x, self.y, 50, 100)
            else:
                if self.jump:
                    self.image.clip_draw(ech_jump[int(self.frame)], 214, ech_jump_w[int(self.frame)], 45,
                                         self.x - self.player.camera_x, self.y, 50, 100)
                else:
                    self.image.clip_draw(ech_run[int(self.frame)], 218, ech_run_w[int(self.frame)], 40,
                                         self.x - self.player.camera_x, self.y, 50, 100)

    def update(self):
        # 게임 시작 시 sonic
        if self.player.start:
            if self.jump:
                self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x += self.speed * RUN_SPEED_PPS * game_framework.frame_time
            if self.jump == False and self.x >= self.exceed_point:
                self.jump = True
                self.frame = 0
            elif self.jump and self.x - self.exceed_point < 50:
                self.y += 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.jump and self.x - self.exceed_point >= 100:
                self.jump = False
                self.frame = 0
                self.exceed_point += 500
            elif self.jump and self.x - self.exceed_point > 50:
                self.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time

        if self.ch_id == 1 and not self.player.start:
            self.frame = (self.frame + 14 * ACTION_PER_TIME * game_framework.frame_time) % 14
        else:
            self.frame = (self.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10

        if self.x >= 5000 and self.finish == False:
            self.finish = True
            print(get_time() - self.time)
