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

def reset_world():
    global running
    global player
    global world
    running = True
    world = []
    player = Player()
    world.append(player)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()

reset_world()

while running:
    handle_event()
    update_world()
    render_world()
    delay(0.05)

close_canvas()