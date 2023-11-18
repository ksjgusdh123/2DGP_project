from pico2d import *

import game_framework
import run_track_mode
import select_menu_mode
import swimming_mode

mode = {'Run': run_track_mode, 'Swim': swimming_mode}
now_map = None
def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

map_num = 0

def init():
    global main_background_image
    global character_result_image
    global font
    global records
    global timer
    global show_score
    show_score = False
    main_background_image = load_image('image/main_background.png')
    character_result_image = load_image('image/result.png')
    font = load_font('font/ENCR10B.TTF', 50)

    records = []
    timer = get_time()
    fill_records(records)

    records.sort()
    run_track_mode.player.score += 1


def finish():
    global records
    records.clear()
def update():
    global show_score
    if get_time() - timer >= 5:
        show_score = True



def draw():
    clear_canvas()
    run_track_mode.result_mode_draw()
    main_background_image.opacify(200/255)
    main_background_image.clip_draw(510, 620, 90, 350, 400, 300, 600, 300)
    if show_score:
        pass
    else:
        records_down_sort_print()

    update_canvas()

def fill_records(records):
        records.append([mode[now_map].player.record, mode[now_map].player.character_id])
        for i in range(3):
            records.append([mode[now_map].ai[i].record, mode[now_map].ai[i].ch_id])

def records_down_sort_print():
    for i in range(0, 3 + 1):
        font.draw(300, 400 - 66 * i, f"{records[i][0]}", (0, 0, 0))
        if records[i][1] == 0:
            character_result_image.clip_draw(80, 326, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif records[i][1] == 1:
            character_result_image.clip_draw(80, 301, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif records[i][1] == 2:
            character_result_image.clip_draw(80, 201, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif records[i][1] == 3:
            character_result_image.clip_draw(80, 276, 81, 26, 170, 400 - 66 * i, 100, 50)


