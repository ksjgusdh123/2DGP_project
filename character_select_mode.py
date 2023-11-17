from pico2d import *
import game_framework
import long_jump_mode

import run_track_mode
import select_level_mode
import select_menu_mode
import swimming_mode

HEIGHT = 600
character_num = None
SONIC = 0
TAILS = 1
SHADOW = 2
ECHDNA = 3

MAP = {'All': run_track_mode, 'hurdle race': run_track_mode, 'swimming': swimming_mode, 'long-jump': long_jump_mode}


def handle_events():
    global running
    global character_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_level_mode)
        elif event.type == SDL_MOUSEMOTION:
            num = 0
            if HEIGHT - event.y < 150:
                num = ECHDNA
            elif HEIGHT - event.y < 300 and HEIGHT - event.y > 150:
                num = SHADOW
            elif HEIGHT - event.y < 450 and HEIGHT - event.y > 300:
                num = TAILS
            elif HEIGHT - event.y < 600 and HEIGHT - event.y > 450:
                num = SONIC
            check_alpha(num)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if HEIGHT - event.y < 150:
                character_num = 3
            elif HEIGHT - event.y < 300 and HEIGHT - event.y > 150:
                character_num = 2
            elif HEIGHT - event.y < 450 and HEIGHT - event.y > 300:
                character_num = 1
            elif HEIGHT - event.y < 600 and HEIGHT - event.y > 450:
                character_num = 0
            if not character_num is None:
                game_framework.change_mode(MAP[select_menu_mode.game_map])


def check_alpha(num):
    for i in range(0, 4):
        if i == num:
            alpha[i] = 255
        else:
            alpha[i] = 128


def init():
    global banner_image
    global running
    global character_num
    global alpha
    character_num = None
    banner_image = load_image('image/banner.png')
    running = True
    alpha = [128, 128, 128, 128]
    if select_menu_mode.game_map is None:
        select_menu_mode.game_map = 'All'

def finish():
    global banner_image
    del banner_image


def update():
    pass


def draw():
    clear_canvas()
    banner_image.opacify(alpha[0] / 255.0)
    banner_image.clip_draw(584, 1202, 288, 72, 400, 525, 800, 150)
    banner_image.opacify(alpha[1] / 255.0)
    banner_image.clip_draw(875, 1202, 288, 72, 400, 375, 800, 150)
    banner_image.opacify(alpha[2] / 255.0)
    banner_image.clip_draw(2, 1052, 288, 72, 400, 225, 800, 150)
    banner_image.opacify(alpha[3] / 255.0)
    banner_image.clip_draw(2, 1127, 288, 72, 400, 75, 800, 150)
    update_canvas()
