from pico2d import *

from player import Player

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


def handle_event():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

def reset_world():
    global running
    global player
    global running_track
    global world
    running = True
    world = []
    player = Player()
    running_track = [Running_track() for i in range(10)]
    world += running_track
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