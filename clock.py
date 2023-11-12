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