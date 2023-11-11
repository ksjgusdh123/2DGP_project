from pico2d import *
import character_select_mode
import game_framework
import game_world
from field import Running_track, Clock
from player import Player
from AI_player import AI

def handle_events():
    global running
    global character_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global running
    global player
    global ai
    global running_track
    running = True
    player = Player(character_select_mode.character_num)
    ai = [AI(player) for _ in range(3)]
    running_track = Running_track(player)
    game_world.add_object(running_track, 0)
    game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


