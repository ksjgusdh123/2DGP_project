import random

from pico2d import *
import game_framework
import character_select_mode
import game_world
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
    global track_image
    global people_image
    global line_image
    global arrow_image
    global obstacle_image
    global command
    track_image = load_image('image/swimming_track.png')
    people_image = load_image('image/running_track.png')
    command = []

    running = True
    player = Player(character_select_mode.character_num)
    player = Player(0)
    ai = [AI(player) for _ in range(3)]
    game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)
    player.y = 100
    ai[0].y = 400
    ai[1].y = 300
    ai[2].y = 200
    player.game_mode = 'swim'
    for i in range(0, 3):
        ai[i].mode = 'swim'


def finish():
    global track_image
    del track_image


def update():
    game_world.update()


def draw():
    clear_canvas()
    draw_simming_track()
    game_world.render()
    update_canvas()

def draw_simming_track():
    track_image.clip_composite_draw(0, 650, 870, 1300, math.pi / 2, '', 250 - player.camera_x, 205, 400, 500)
    for i in range(1, 20 + 1):
        track_image.clip_composite_draw(0, 400, 870, 550, math.pi / 2, '', 500 * i - player.camera_x, 205, 400, 500)
        people_image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - player.camera_x, 500, 1024, 200)
