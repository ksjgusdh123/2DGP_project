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

def init():
    global main_background_image
    global sports_pictogram
    global running
    global font
    main_background_image = load_image('image/main_background.png')
    sports_pictogram = load_image('image/pictogram.png')
    running = True
    font = load_font('font/ENCR10B.TTF', 30)
def finish():
    global main_background_image
    global sports_pictogram
    del main_background_image
    del sports_pictogram

def update():
    pass

def draw():
    clear_canvas()
    main_background_image.clip_draw(0, 620, 220, 350, 150, 300, 300, 600)
    main_background_image.clip_draw(510, 620, 90, 350, 550, 300, 500, 600)
    sports_pictogram.clip_draw(260, 65, 65, 65, 550, 400, 100,100)
    update_canvas()


