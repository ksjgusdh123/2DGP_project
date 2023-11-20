import random

from pico2d import *
import game_framework
import character_select_mode
import game_world
import middle_result_mode
import run_track_mode
import select_level_mode
import select_menu_mode
from clock import Clock
from player import Player
from AI_player import AI

player = None
ai = [None, None, None]
level = {'easy': 2, 'normal': 3, 'hard': 4}

def handle_events():
    global running
    global character_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_menu_mode)
            delete_object()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            if player.shooting_pos[1] <= 1:
                player.shooting_pos[1] += 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if player.shooting_pos[1] > 0:
                player.shooting_pos[1] -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            if player.shooting_pos[0] > 0:
                player.shooting_pos[0] -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            if player.shooting_pos[0] <= 1:
                player.shooting_pos[0] += 1
        elif not clock is None and event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            player.ready = True
            clock.start = True
            print('clock spone')
        else:
            player.handle_event(event)


def init():
    global running
    global player
    global ai
    global track_image
    global rectangle_image
    global red_rectangle_image
    global shooting_target_image
    global clock
    global font
    font = load_font('font/ENCR10B.TTF', 50)
    track_image = load_image('image/shooting_background_image.png')
    rectangle_image = load_image('image/rectangle.png')
    red_rectangle_image = load_image('image/red_rectangle1.png')
    shooting_target_image = load_image('image/target.png')
    middle_result_mode.now_map = 'Shooting'
    clock = Clock()
    game_world.add_object(clock, 0)

    if not select_menu_mode.game_map == 'All':
        # player = Player(character_select_mode.character_num)
        player = Player(0)
        ai = [AI(player) for _ in range(3)]
        game_world.add_objects(ai, 1)
        game_world.add_object(player, 1)
        for i in range(0, 3):
            ai[i].y = -100
            ai[i].x = -100
            ai[i].mode = 'shooting'
    else:
        player = run_track_mode.player
        for i in range(3):
            ai[i] = run_track_mode.ai[i]
            ai[i].mode = 'shooting'
            ai[i].y = -100
            ai[i].x = -100
            ai[i].finish = False
    player.game_mode = 'shooting'


def delete_object():
    global player
    global ai
    ai[0].delete_ai()
    for i in range(3):
        game_world.remove_object(ai[i])
    for i in range(3):
        del ai[0]
    ai = [None, None, None]
    game_world.remove_object(player)
    player = None

def finish():
    global clock
    player.start = False
    player.ready = False
    if clock:
        game_world.remove_object(clock)
    pass

def update():
    clock_update()
    game_world.update()


def draw():
    clear_canvas()
    track_image.clip_draw(110, 0, 550, 135, 400, 300, 800, 600)
    game_world.render()
    rectangle_draw()
    shooting_target_image.draw(400, 300, 100, 100)
    update_canvas()


def map_timer_draw():
    if player.start == False:
        font.draw(300, 550, f"0:000", (0, 0, 0))
    else:
        font.draw(300, 550, f"{get_time() - player.time:.3f}", (0, 0, 0))



def rectangle_draw():
    for i in range(3):
        for j in range(3):
            if player.shooting_pos[0] == j and player.shooting_pos[1] == i:
                red_rectangle_image.clip_draw(34, 11, 170, 189, (i + 1) * 150 + 100, (j + 1) * 150 + 80, 120, 120)
            else:
                rectangle_image.draw((i + 1) * 150 + 100, (j + 1) * 150 + 80, 150, 150)

def track_update():
    pass

def clock_update():
    global clock
    if not clock is None:
        if clock.interval >= 3:
            player.start = True
            player.time = get_time()
            for i in range(0, 3):
                ai[i].time = player.time
            game_world.remove_object(clock)
            clock = None
