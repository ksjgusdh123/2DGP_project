from pico2d import *

from field import Running_track, Clock
from player import Player
from AI_player import AI


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
    global ai
    global running_track
    global clock
    global world
    running = True
    world = []
    player = Player()
    ai = AI(player)
    clock = Clock(player)
    running_track = Running_track(player)
    world.append(running_track)
    world.append(clock)
    world.append(ai)
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