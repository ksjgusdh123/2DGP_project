import random
import math
from pico2d import load_image

class Running_track:
    num = -1
    command = []
    def __init__(self, player):
        self.image = load_image('running_track.png')
        self.obstacle = load_image('obstacle.png')
        self.arrow = load_image('arrow.png')
        Running_track.num += 1
        self.track_num = Running_track.num
        self.player = player
    def draw(self):
        self.image.clip_draw(26, 126, 254, 100, 254 * self.track_num - self.player.camera_x, 200, 254, 500)
        self.image.clip_draw(28, 236, 208, 64, 1024 * (self.track_num // 4) - self.player.camera_x, 500, 1024, 200)
        self.obstacle.draw(300 - self.player.camera_x, 120, 100, 100)
        for i in range(0, len(Running_track.command)):
            if Running_track.command[i] == 0:
                self.arrow.clip_composite_draw(0, 0, 670, 373, 0, ' ', self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
            elif Running_track.command[i] == 1:
                self.arrow.clip_composite_draw(0, 0, 670, 373, 0, 'h', self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
            elif self.command[i] == 2:
                self.arrow.clip_composite_draw(0, 0, 670, 373, math.pi / 2, '', self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
            elif self.command[i] == 3:
                self.arrow.clip_composite_draw(0, 0, 670, 373, math.pi / 2, 'h', self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)

    def update(self):
        if self.player.x + 100 > 300:
            if len(Running_track.command) == 0:
                Running_track.command= [random.randint(0, 3) for n in range(2)]
