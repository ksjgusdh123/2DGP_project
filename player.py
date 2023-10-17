from pico2d import load_image


class Player:
    def __init__(self):
        self.image = load_image('sonic_animation.png')
        self.frame = 0
        self.x, self.y = 100, 100
    def update(self):
        self.frame = (self.frame + 1) % 10
    def draw(self):
        self.image.clip_draw(self.frame // 2 * 22 + 5, 249, 18, 30, self.x, self.y, 50, 100)
