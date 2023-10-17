from pico2d import load_image


class Running_track:
    num = -1
    def __init__(self, player):
        self.image = load_image('running_track.png')
        self.obstacle = load_image('obstacle.png')
        Running_track.num += 1
        self.track_num = Running_track.num
        self.player = player
    def draw(self):
        self.image.clip_draw(26, 126, 254, 100, 254 * self.track_num - self.player.camera_x, 200, 254, 500)
        self.image.clip_draw(28, 236, 208, 64, 1024 * (self.track_num // 4) - self.player.camera_x, 500, 1024, 200)
        self.obstacle.draw(300 - self.player.camera_x, 120, 100, 100)

    def update(self):
        pass
