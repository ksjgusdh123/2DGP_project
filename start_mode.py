from pico2d import *

import character_select_mode
import game_framework

import run_track_mode

HEIGHT = 600
character_num = 100

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(character_select_mode)

def init():
    global main_background_image
    global running
    main_background_image = load_image('image/test3.png')
    running = True

def finish():
    global main_background_image
    del main_background_image

def update():
    pass

def draw():
    clear_canvas()
    main_background_image.clip_draw(604, 553, 422, 419, 400, 300, 800, 600)
    update_canvas()


