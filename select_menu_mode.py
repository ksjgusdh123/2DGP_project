from pico2d import *

import character_select_mode
import game_framework

import run_track_mode
import select_level_mode
import start_game_mode

HEIGHT = 600
character_num = 100
picture_size = 75
pictogram_start_x = 350
game_map = None
game_maps = ['shooting', 'long-jump', 'swimming', 'hurdle race', 'All']
def handle_events():
    global running
    global game_map

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(start_game_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and pictogram_start_x - picture_size / 2 <= event.x <= pictogram_start_x + picture_size / 2:
            for i in range(1, 5 + 1):
                if i * 100 - picture_size / 2 <= HEIGHT - event.y <= i * 100 + picture_size / 2:
                    game_map = game_maps[i - 1]
                    game_framework.change_mode(select_level_mode)
                    print(game_map)
    if not game_map == None:
        start_game_mode.main_bgm.play()




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
    global font
    del font
    del main_background_image
    del sports_pictogram

def update():
    pass


def draw():
    clear_canvas()
    draw_image()
    draw_font()
    update_canvas()


def draw_image():
    main_background_image.clip_draw(0, 620, 220, 350, 150, 300, 300, 600)
    main_background_image.clip_draw(510, 620, 90, 350, 550, 300, 500, 600)
    sports_pictogram.clip_draw(130, 130, 65, 65, pictogram_start_x, 100, picture_size, picture_size)
    sports_pictogram.clip_draw(0, 65, 65, 65, pictogram_start_x, 200, picture_size, picture_size)
    sports_pictogram.clip_draw(260, 260, 65, 65, pictogram_start_x, 300, picture_size, picture_size)
    sports_pictogram.clip_draw(260, 65, 65, 65, pictogram_start_x, 400, picture_size, picture_size)
    sports_pictogram.clip_draw(0, 260, 65, 65, pictogram_start_x, 500, picture_size, picture_size)


def draw_font():
    font.draw(400, 100, f'Clay-pigeon shooting', (0, 0, 0))
    font.draw(400, 200, f'long-jump', (0, 0, 0))
    font.draw(400, 300, f'swimming', (0, 0, 0))
    font.draw(400, 400, f'hurdle race', (0, 0, 0))
    font.draw(400, 500, f'All', (0, 0, 0))
    font.draw(430, 570, f'select game mode', (0, 0, 0))


