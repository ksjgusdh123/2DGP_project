from pico2d import *

import character_select_mode
import game_framework

import select_menu_mode

HEIGHT = 600
picture_size = 75
pictogram_start_x = 350
game_level = None
def handle_events():
    global running
    global game_level
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_menu_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if 550 <= event.x <= 745:
                if 70 <= HEIGHT - event.y <= 130:
                    game_level = 'hard'
                elif 220 <= HEIGHT - event.y <= 280:
                    game_level = 'normal'
                elif 370 <= HEIGHT - event.y <= 430:
                    game_level = 'easy'
                if not game_level is None:
                    game_framework.change_mode(character_select_mode)

def init():
    global main_background_image
    global sports_pictogram
    global run_screenshot
    global long_jump_screenshot
    global shooting_screenshot
    global level_box
    global running
    global font
    global mini_font
    main_background_image = load_image('image/main_background.png')
    sports_pictogram = load_image('image/pictogram.png')
    level_box = load_image('image/rectangle.png')
    run_screenshot = load_image('image/run_screen_shot.png')
    long_jump_screenshot = load_image('image/long_jump_screen_shot.png')
    shooting_screenshot = load_image('image/shooting_screen_shot.png')
    running = True
    font = load_font('font/ENCR10B.TTF', 50)
    mini_font = load_font('font/ENCR10B.TTF', 20)
    if select_menu_mode.game_map == None:
        select_menu_mode.game_map = 'All'
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
    draw_UI()
    update_canvas()


def draw_UI():
    main_background_image.clip_draw(510, 620, 90, 350, 400, 300, 800, 600)
    if select_menu_mode.game_map == 'All':
        sports_pictogram.clip_draw(0, 260, 65, 65, pictogram_start_x - 50, 550, picture_size, picture_size)
        font.draw(400, 550, f'All', (0, 0, 0))
    elif select_menu_mode.game_map == 'hurdle race':
        sports_pictogram.clip_draw(260, 65, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        run_screenshot.draw(250, 350, 400, 200)
        font.draw(300, 550, f'hurdle race', (0, 0, 0))
        mini_font.draw(50, 200, f'', (0, 0, 0))
    elif select_menu_mode.game_map == 'swimming':
        sports_pictogram.clip_draw(260, 260, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        font.draw(300, 550, f'swimming', (0, 0, 0))
        mini_font.draw(50, 200, f'', (0, 0, 0))
    elif select_menu_mode.game_map == 'long-jump':
        sports_pictogram.clip_draw(0, 65, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        long_jump_screenshot.draw(250, 350, 400, 200)
        font.draw(300, 550, f'long-jump', (0, 0, 0))
        mini_font.draw(50, 200, f'', (0, 0, 0))
    elif select_menu_mode.game_map == 'shooting':
        sports_pictogram.clip_draw(130, 130, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        shooting_screenshot.draw(250, 350, 400, 200)
        font.draw(300, 550, f'shooting', (0, 0, 0))
        mini_font.draw(50, 200, f'', (0, 0, 0))

    level_box.draw(250, 130, 600, 300)

    level_box.draw(650, 400, 250, 70)
    level_box.draw(650, 250, 250, 70)
    level_box.draw(650, 100, 250, 70)
    font.draw(590, 100, f'hard', (0, 0, 0))
    font.draw(565, 250, f'normal', (0, 0, 0))
    font.draw(590, 400, f'easy', (0, 0, 0))





