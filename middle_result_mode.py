from pico2d import *

import game_framework
import long_jump_mode
import run_track_mode
import select_menu_mode
import swimming_mode

mode = {'Run': run_track_mode, 'Swim': swimming_mode, 'long-jump': long_jump_mode}
now_map = None
scores = []


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if now_map == 'long-jump' and long_jump_mode.jump_chance > 0:
                game_framework.change_mode(long_jump_mode)
            elif select_menu_mode.game_map == 'All':
                if mode[now_map].player.next_map == 'swim':
                    game_framework.change_mode(swimming_mode)
                elif mode[now_map].player.next_map == ('long-jump'):
                    game_framework.change_mode(long_jump_mode)
            else:
                mode[now_map].delete_object()
                game_framework.change_mode(select_menu_mode)

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

    fill_records()
    if now_map == 'long-jump':
        records.sort(reverse=True)
    else:
        records.sort()
    if not now_map == 'long-jump' or long_jump_mode.jump_chance < 1:
        score_plus()
    fill_scores()
    scores.sort(reverse=True)



def finish():
    global records
    global scores
    records.clear()
    scores.clear()

def update():
    global show_score
    if get_time() - timer >= 5:
        show_score = True



def draw():
    clear_canvas()
    mode[now_map].result_mode_draw()
    main_background_image.opacify(200/255)
    main_background_image.clip_draw(510, 620, 90, 350, 400, 300, 600, 300)
    if show_score:
        scores_up_sort_print()
    else:
        records_down_sort_print()
    update_canvas()


def fill_records():
        records.append([mode[now_map].player.record, mode[now_map].player.character_id])
        for i in range(3):
            records.append([mode[now_map].ai[i].record, mode[now_map].ai[i].ch_id])

def fill_scores():
    scores.append([mode[now_map].player.score, mode[now_map].player.character_id])
    for i in range(3):
        scores.append([mode[now_map].ai[i].score, mode[now_map].ai[i].ch_id])

def scores_up_sort_print():
    for i in range(0, 3 + 1):
        font.draw(300, 400 - 66 * i, f'{scores[i][0]}', (0, 0, 0))
        if scores[i][1] == 0:
            character_result_image.clip_draw(80, 326, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif scores[i][1] == 1:
            character_result_image.clip_draw(80, 301, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif scores[i][1] == 2:
            character_result_image.clip_draw(80, 201, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif scores[i][1] == 3:
            character_result_image.clip_draw(80, 276, 81, 26, 170, 400 - 66 * i, 100, 50)


def records_down_sort_print():
    for i in range(0, 3 + 1):
        font.draw(300, 400 - 66 * i, f"{records[i][0]:.4f}", (0, 0, 0))
        if records[i][1] == 0:
            character_result_image.clip_draw(80, 326, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif records[i][1] == 1:
            character_result_image.clip_draw(80, 301, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif records[i][1] == 2:
            character_result_image.clip_draw(80, 201, 81, 26, 170, 400 - 66 * i, 100, 50)
        elif records[i][1] == 3:
            character_result_image.clip_draw(80, 276, 81, 26, 170, 400 - 66 * i, 100, 50)


def score_plus():
    for i in range(0, 3 + 1):
        if records[i][1] == mode[now_map].player.character_id:
            mode[now_map].player.score += 10 - 3 * i

        for j in range(3):
            if mode[now_map].ai[j].ch_id == records[i][1]:
                mode[now_map].ai[j].score += 10 - 3 * i
                break