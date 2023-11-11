import random
import math
from pico2d import load_image, get_time

import game_world


class Clock:
    def __init__(self, player):
        self.start_time = get_time()
        self.number = load_image('image/number.png')
        self.idx = 0
        self.player = player

    def draw(self):
        if self.idx <= 3:
            self.number.clip_composite_draw(21, 157 - self.idx * 65, 44, 43, -math.pi / 2, '', 400, 400, 100, 100)

    def update(self):
        interval = get_time() - self.start_time
        if interval > 3:
            self.player.start = True

            game_world.remove_object(self)

        elif interval >= 2:
            self.idx = 2
        elif interval >= 1:
            self.idx = 1
        else:
            self.idx = 0


class Running_track:
    def __init__(self, player):
        self.image = load_image('image/running_track.png')
        self.obstacle = load_image('image/obstacle.png')
        self.arrow = load_image('image/arrow.png')
        self.line = load_image('image/finishline.png')
        self.command = []
        self.player = player
        self.mode = 2
        self.start_time = get_time()

    def draw(self):
        for i in range(0, 21):
            self.image.clip_draw(26, 126, 254, 100, 254 * i - self.player.camera_x, 200, 254, 500)
            self.image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - self.player.camera_x, 500, 1024, 200)

        self.line.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 200 - self.player.camera_x, 190, 250,
                                      100)
        self.line.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 5000 - self.player.camera_x, 190, 250,
                                      100)
        for i in range(1000, 5000 - 1, 500):
            for j in range(0, 4):
                self.obstacle.draw(i - self.player.camera_x, 120 + 50 * j + j * 10, 100, 100)
        self.arrow_draw()

    def arrow_draw(self):
        for i in range(0, len(self.command)):
            if self.command[i] == 0:
                self.arrow.clip_composite_draw(0, 0, 670, 373, 0, ' ',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
            elif self.command[i] == 1:
                self.arrow.clip_composite_draw(0, 0, 670, 373, 0, 'h',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
            elif self.command[i] == 2:
                self.arrow.clip_composite_draw(0, 0, 670, 373, math.pi / 2, '',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
            elif self.command[i] == 3:
                self.arrow.clip_composite_draw(0, 0, 670, 373, math.pi / 2, 'h',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)

    def update(self):
        if self.player.x + 100 > self.player.exceed_point and self.player.success == False:
            if len(self.command) == 0:
                self.command = [random.randint(0, 3) for n in
                                range(random.randint(self.mode + 1, self.mode + 3))]
        elif self.player.x < self.player.exceed_point - 100:
            self.command.clear()
            self.player.input_command.clear()
            self.player.success = False
            self.player.perfect = True

        if (len(self.command) != 0 and len(self.player.input_command) != 0):
            if self.command[0] == self.player.input_command[0] and self.player.perfect:
                del self.command[0]
                self.player.input_command.clear()
            else:
                self.player.perfect = False
            if len(self.command) == 0 and self.player.perfect == True:
                self.player.success = True
