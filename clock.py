import math
from pico2d import load_image, get_time

import game_world


class Clock:
    def __init__(self):
        self.start_time = get_time()
        self.number = load_image('image/number.png')
        self.idx = 0
        self.interval = 0
        self.start = False
        self.init = False
    def draw(self):
        if self.idx <= 3 and self.start:
            self.number.clip_composite_draw(21, 157 - self.idx * 65, 44, 43, -math.pi / 2, '', 400, 400, 100, 100)

    def update(self):

        if self.start:
            if not self.init:
                self.init = True
                self.interval = 0
                self.start_time = get_time()
            self.interval = get_time() - self.start_time
            if self.init:
                if self.interval >= 2:
                    self.idx = 2
                elif self.interval >= 1:
                    self.idx = 1
                else:
                    self.idx = 0