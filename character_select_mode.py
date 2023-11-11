from pico2d import *
import game_framework

import play_mode

HEIGHT = 600
character_num = 100

def handle_events():
    global running
    global character_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if HEIGHT - event.y < 150:
                character_num = 3
                game_framework.change_mode(play_mode)
            elif HEIGHT - event.y < 300 and HEIGHT - event.y > 150:
                character_num = 2
                game_framework.change_mode(play_mode)
            elif HEIGHT - event.y < 450 and HEIGHT - event.y > 300:
                character_num = 1
                game_framework.change_mode(play_mode)
            elif HEIGHT - event.y < 600 and HEIGHT - event.y > 450:
                character_num = 0
                game_framework.change_mode(play_mode)


def init():
    global banner_image
    global running
    global character_num

    character_num = None
    banner_image = load_image('image/banner.png')
    running = True

def finish():
    global banner_image
    del banner_image

def update():
    pass

def draw():
    clear_canvas()
    banner_image.clip_draw(584, 1202, 288, 72, 400, 525, 800, 150)
    banner_image.clip_draw(875, 1202, 288, 72, 400, 375, 800, 150)
    banner_image.clip_draw(2, 1052, 288, 72, 400, 225, 800, 150)
    banner_image.clip_draw(2, 1127, 288, 72, 400, 75, 800, 150)
    update_canvas()


