from pico2d import *

import game_world
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
    # global clock
    running = True

    player = Player()
    ai = [AI(player) for i in range(3)]
    # clock = Clock(player)
    running_track = Running_track(player)
    game_world.add_object(running_track, 0)
    # game_world.add_object(clock, 1)
    game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)

def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

open_canvas()

reset_world()

while running:
    handle_event()
    update_world()
    render_world()
    delay(0.05)

close_canvas()