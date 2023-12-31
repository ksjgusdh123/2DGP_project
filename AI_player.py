import random

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

SONIC = 0
TAILS = 1
SHADOW = 2
ECHDNA = 3


class AI:
    ai_num = 0
    num = -1

    def __init__(self, player):
        self.player = player

        if self.player.character_id == SONIC:
            if AI.ai_num == 0:
                AI.ai_num += 1
                self.image = load_image('image/tails.png')
            elif AI.ai_num == 2:
                self.image = load_image('image/shadow.png')
            elif AI.ai_num == 3:
                self.image = load_image('image/echidna.png')
        elif self.player.character_id == TAILS:
            if AI.ai_num == 0:
                self.image = load_image('image/sonic_animation.png')
            elif AI.ai_num == 1:
                AI.ai_num += 1
                self.image = load_image('image/shadow.png')
            elif AI.ai_num == 3:
                self.image = load_image('image/echidna.png')
        elif self.player.character_id == SHADOW:
            if AI.ai_num == 0:
                self.image = load_image('image/sonic_animation.png')
            elif AI.ai_num == 1:
                self.image = load_image('image/tails.png')
            elif AI.ai_num == 2:
                AI.ai_num += 1
                self.image = load_image('image/echidna.png')
        elif self.player.character_id == ECHDNA:
            if AI.ai_num == 0:
                self.image = load_image('image/sonic_animation.png')
            elif AI.ai_num == 1:
                self.image = load_image('image/tails.png')
            elif AI.ai_num == 2:
                self.image = load_image('image/shadow.png')
        AI.ai_num += 1
        AI.num += 1
        self.temp_num = AI.num
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
        self.first_record = 0
        self.second_record = 0
        self.record = self.ch_id
        self.score = 0
        self.left_bullet = 20

    def delete_ai(self):
        AI.num = -1
        AI.ai_num = 0

    def draw(self):
        self.draw_character()

    def draw_character(self):
        if self.ch_id == SONIC:
            if ((not self.player.start or self.finish) and not self.mode == 'swim') or self.mode == 'shooting':
                self.image.clip_draw(int(self.frame) // 2 * 22 + 5, 249, 18, 30, self.x - self.player.camera_x, self.y,
                                     50, 100)
            else:
                if self.mode == 'run':
                    if self.jump:
                        self.image.clip_draw(sonic_jump[int(self.frame)], 215, sonic_jump_w[int(self.frame)], 30,
                                             self.x - self.player.camera_x, self.y, 50, 100)
                    else:
                        self.image.clip_draw(sonic_run[int(self.frame)], 149, 23, 27, self.x - self.player.camera_x,
                                             self.y, 50, 100)
                elif self.mode == 'swim':
                    self.image.clip_draw(sonic_swim[int(self.frame)], 57, 36, 20,
                                                self.x - self.player.camera_x, self.y, 50, 100)

        elif self.ch_id == TAILS:
            if ((not self.player.start or self.finish) and not self.mode == 'swim') or self.mode == 'shooting':
                self.image.clip_draw(int(self.frame) // 2 * 32 + 107, 960, 21, 35, self.x - self.player.camera_x,
                                     self.y, 50, 100)
            else:
                if self.mode == 'run':
                    if self.jump:
                        self.image.clip_draw(tails_jump[int(self.frame)], 736, tails_jump_w[int(self.frame)], 32,
                                             self.x - self.player.camera_x, self.y, 50, 100)
                    else:
                        self.image.clip_draw(tails_run[int(self.frame)], 784, 36, 35, self.x - self.player.camera_x,
                                             self.y, 50, 100)
                elif self.mode == 'swim':
                    self.image.clip_composite_draw(tails_swim[int(self.frame)], 264, 40, 30, 3.14 * 30, 'h',
                                                          self.x - self.player.camera_x, self.y, 50, 100)


        elif self.ch_id == SHADOW:
            if ((not self.player.start or self.finish) and not self.mode == 'swim') or self.mode == 'shooting':
                self.image.clip_draw(int(self.frame) // 2 * 26 + 6, 467, 23, 33, self.x - self.player.camera_x, self.y,
                                     50, 100)
            else:
                if self.mode == 'run':
                    if self.jump:
                        self.image.clip_draw(shadow_jump[int(self.frame)], 317, shadow_jump_w[int(self.frame)], 39,
                                             self.x - self.player.camera_x, self.y, 50, 100)
                    else:
                        self.image.clip_draw(shadow_run[int(self.frame)], 431, shadow_run_w[int(self.frame)], 32,
                                             self.x - self.player.camera_x, self.y, 50, 100)
                elif self.mode == 'swim':
                    self.image.clip_composite_draw(shadow_swim[int(self.frame)], 284, 38, 30, 3.14 * 30, 'h',
                                                          self.x - self.player.camera_x, self.y, 50, 100)

        if self.ch_id == ECHDNA:
            if ((not self.player.start or self.finish) and not self.mode == 'swim') or self.mode == 'shooting':
                self.image.clip_draw(int(self.frame) // 2 * 31 + 117, 262, 29, 42, self.x - self.player.camera_x,
                                     self.y, 50, 100)
            else:
                if self.mode == 'run':
                    if self.jump:
                        self.image.clip_draw(ech_jump[int(self.frame)], 214, ech_jump_w[int(self.frame)], 45,
                                             self.x - self.player.camera_x, self.y, 50, 100)
                    else:
                        self.image.clip_draw(ech_run[int(self.frame)], 218, ech_run_w[int(self.frame)], 40,
                                             self.x - self.player.camera_x, self.y, 50, 100)
                elif self.mode == 'swim':
                    self.image.clip_draw(ech_swim[int(self.frame)], 51, 50, 25,
                                                self.x - self.player.camera_x,
                                                self.y, 50, 100)

    def get_time(self):
        self.time = self.player.time

    def update(self):
        if self.mode == 'run':
            self.running_track_update()
        elif self.mode == 'swim':
            self.swim_update()
        elif self.mode == 'shooting':
            self.shooting_update()

    def shooting_update(self):
        self.basic_update()

    def get_record(self):
        num = random.randint(1, 2)
        if num == 1:
            self.record += 1
            self.left_bullet -= 1
        else:
            num = random.randint(1, 2)
            if num == 1:
                self.left_bullet -= 1

    def swim_update(self):
        if self.player.start and not self.finish:
            self.x += self.speed * RUN_SPEED_PPS * game_framework.frame_time
        self.basic_update()

    def running_track_update(self):
        if self.player.start and not self.finish:
            if self.jump:
                self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.x += self.speed * RUN_SPEED_PPS * game_framework.frame_time
            if self.jump == False and self.x >= self.exceed_point:
                self.jump = True
                self.frame = 0
            if self.jump and self.x - self.exceed_point < 50:
                self.y += 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.jump and self.x - self.exceed_point >= 100:
                self.jump = False
                self.frame = 0
                if self.exceed_point <= 4000:
                    self.exceed_point += 500
                else:
                    self.exceed_point = 10000
            elif self.jump and self.x - self.exceed_point > 50:
                self.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time
        self.basic_update()


    def basic_update(self):
        if self.ch_id == 1 and not self.mode == 'swim':
            if not self.player.start or self.finish:
                self.frame = (self.frame + 14 * ACTION_PER_TIME * game_framework.frame_time) % 14
            else:
                self.frame = (self.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        else:
            self.frame = (self.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        if self.x >= 5000 and self.finish == False:
            self.finish = True
            self.record = get_time() - self.time
            self.frame = 0
            print(get_time() - self.time)

