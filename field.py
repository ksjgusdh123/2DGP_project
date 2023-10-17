from pico2d import load_image


class Running_track:
    num = -1
    def __init__(self):
        self.image = load_image('running_track.png')
        Running_track.num += 1
        self.track_num = Running_track.num
    def draw(self):
        self.image.clip_draw(26, 126, 254, 100, 254 * self.track_num, 200, 254, 500)
        self.image.clip_draw(28, 236, 208, 64, 1024 * (self.track_num // 4), 500, 1024, 200)

    def update(self):
        pass
