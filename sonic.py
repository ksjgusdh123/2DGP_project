from pico2d import *

class Player:
    def __init__(self):
        self.image = load_image('sonic_animation.png')
        self.frame = 0
        self.x, self.y = 100, 100
    def update(self):
        self.frame = (self.frame + 1) % 10
    def draw(self):
        self.image.clip_draw(self.frame // 2 * 22 + 5, 249, 18, 30, self.x, self.y, 50, 100)
def handle_event():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

running = True

open_canvas()
player = Player()
while running:
    player.draw()
    handle_event()
    update_canvas()
    pass

close_canvas()