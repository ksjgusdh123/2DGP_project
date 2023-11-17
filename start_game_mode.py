from pico2d import *

import game_framework

import select_menu_mode

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
            game_framework.change_mode(select_menu_mode)

def init():
    global main_background_image
    global running
    global font
    main_background_image = load_image('image/main_background.png')
    running = True
    font = load_font('font/ENCR10B.TTF', 30)

def finish():
    global main_background_image
    global font
    del font
    del main_background_image

def update():
    pass

def draw():
    clear_canvas()
    main_background_image.clip_draw(604, 553, 422, 419, 400, 300, 800, 600)
    font.draw(330, 100, f'press the space',(0,0,0))
    update_canvas()


