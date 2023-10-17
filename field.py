import random
import math
from pico2d import load_image, get_time

class Clock:
    def __init__(self, player):
        self.start_time = get_time()
        self.number = load_image('number.png')
        self.idx = 0
        self.player = player
    def draw(self):
        if self.idx <= 3:
            self.number.clip_composite_draw(21, 157 - self.idx * 65, 44, 43, -math.pi / 2, '', 400, 400, 100, 100)
    def update(self):
        if self.idx <= 3:
            interval = get_time() - self.start_time
            if interval > 3:
                self.player.start = True
                self.idx = 1000
            elif interval >= 2:
                self.idx = 2
            elif interval >= 1:
                self.idx = 1
            else:
                self.idx = 0


        pass

class Running_track:
    num = -1
    command = []
    image = None
    obstacle = None
    arrow = None
    line = None
    def __init__(self, player):
        if Running_track.image  == None:
            Running_track.image = load_image('running_track.png')
        if Running_track.obstacle  == None:
            Running_track.obstacle = load_image('obstacle.png')
        if Running_track.arrow  == None:
            Running_track.arrow = load_image('arrow.png')
        if Running_track.line  == None:
            Running_track.line = load_image('finishline.png')
        Running_track.num += 1
        self.track_num = Running_track.num
        self.player = player
        self.mode = 2
        self.start_time = get_time()
    def draw(self):
        Running_track.image.clip_draw(26, 126, 254, 100, 254 * self.track_num - self.player.camera_x, 200, 254, 500)
        Running_track.image.clip_draw(28, 236, 208, 64, 1024 * (self.track_num // 4) - self.player.camera_x, 500, 1024, 200)
        if self.track_num == 20:
            Running_track.line.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 200 - self.player.camera_x, 190, 250, 100)
            Running_track.line.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 5000 - self.player.camera_x, 190, 250, 100)
            for i in range(1000, 5000 - 1, 500):
                for j in range(0, 4):
                    Running_track.obstacle.draw(i - self.player.camera_x, 120 + 50 * j + j * 10, 100, 100)
            self.arrow_draw()

    def arrow_draw(self):
        if self.track_num == 20:
            for i in range(0, len(Running_track.command)):
                if Running_track.command[i] == 0:
                    Running_track.arrow.clip_composite_draw(0, 0, 670, 373, 0, ' ',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
                elif Running_track.command[i] == 1:
                    Running_track.arrow.clip_composite_draw(0, 0, 670, 373, 0, 'h',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
                elif Running_track.command[i] == 2:
                    Running_track.arrow.clip_composite_draw(0, 0, 670, 373, math.pi / 2, '',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)
                elif Running_track.command[i] == 3:
                    Running_track.arrow.clip_composite_draw(0, 0, 670, 373, math.pi / 2, 'h',
                                               self.player.x + i * 100 - 50 - self.player.camera_x,
                                               self.player.y + 100, 100, 100)

    def update(self):
        if self.player.x + 100 > self.player.exceed_point and self.player.success == False:
            if len(Running_track.command) == 0:
                Running_track.command= [random.randint(0, 3) for n in range(random.randint(self.mode + 1, self.mode + 3))]
        elif self.player.x < self.player.exceed_point - 100:
            Running_track.command.clear()
            self.player.input_command.clear()
            self.player.success = False
            self.player.perfect = True

        if(len(Running_track.command) != 0 and len(self.player.input_command) !=0):
            if Running_track.command[0] == self.player.input_command[0] and self.player.perfect:
                del Running_track.command[0]
                self.player.input_command.clear()
            else:
                self.player.perfect = False
            if len(Running_track.command) == 0 and self.player.perfect == True:
                self.player.success = True
            