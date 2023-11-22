import random

from pico2d import load_image
import select_level_mode
import game_framework
import select_menu_mode

level = {'easy': 2, 'normal': 4, 'hard': 6}
PIXEL_PER_METER = 10 / 0.3
RUN_SPEED_KMPH = 20
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000 / 60
RUN_SPEED_MPS = RUN_SPEED_MPM / 60
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER
if select_level_mode.game_level == None:
    select_level_mode.game_level = 'hard'

class Target:
    image = None
    def __init__(self):
        num = random.randint(1, 2)
        if num == 1:
            self.x = 0
            self.is_left = True
        elif num == 2:
            self.x = 800
            self.is_left = False
        self.y = random.randint(500, 600)
        # self.y = 230 + 90
        self.speed = random.randint(1 + level[select_level_mode.game_level], 5 + level[select_level_mode.game_level])
        self.down_speed = random.randint(1, 3)
        self.pos = [-1, -1]
        self.delete = False
        self.skip = False

        if Target.image == None:
            Target.image = load_image('image/target.png')

    def draw(self):
        self.image.draw(self.x, self.y, 75, 75)


    def update(self):
        if self.is_left:
            self.x += self.speed * 1 * RUN_SPEED_PPS * game_framework.frame_time
            # self.x = 351
        else:
            # self.x = 351
            self.x -= self.speed * 1 * RUN_SPEED_PPS * game_framework.frame_time
        # self.y = 179
        self.y -= self.down_speed * 1 * RUN_SPEED_PPS * game_framework.frame_time
        for i in range(3):
            for j in range(3):
                if ((j + 1) * 150 + 50 < self.x < (j + 1) * 150 + 150
                        and (i + 1) * 150 + 30 < self.y < (i + 1) * 150 + 130):
                            self.pos[0] = i
                            self.pos[1] = j

        if self.is_left:
            if self.x >= 800:
                self.delete = True
        else:
            if self.x <= 0:
                self.delete = True
        if self.y <= 0:
            self.delete = True

        if self.delete:
            if self.pos[0] == -1 and self.pos[1] == -1:
                self.skip = True


