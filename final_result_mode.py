from pico2d import *

import game_framework
import game_world
import long_jump_mode
import run_track_mode
import select_menu_mode
import start_game_mode
import swimming_mode
from AI_player import AI
from player import Player

scores = []

SONIC = 0
TAILS = 1
SHADOW = 2
ECHDNA = 3

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            delete_object()
            game_framework.change_mode(start_game_mode)


def init():
    global main_background_image
    global character_result_image
    global effect_image
    global font
    global timer
    global temp_player
    global temp_ai
    main_background_image = load_image('image/ending_background.png')
    effect_image = load_image('image/effect.png')
    character_result_image = load_image('image/result.png')
    font = load_font('font/ENCR10B.TTF', 40)

    timer = get_time()

    temp_player = Player(0)
    temp_ai = [AI(temp_player) for _ in range(3)]
    game_world.add_objects(temp_ai, 1)
    game_world.add_object(temp_player, 1)

    temp_player.score = 19
    temp_player.game_mode = 'run'
    for i in range(3):
        temp_ai[i].score = i + 2
        temp_ai[i].mode = 'run'
    fill_scores()
    scores.sort(reverse=True)

def finish():
    global scores
    scores.clear()

def update():
    game_world.update()
    pass

def draw():
    clear_canvas()
    main_background_image.clip_draw(440, 10, 420, 230, 400, 300, 800, 600)
    scores_down_sort_print()
    game_world.render()
    medal_draw()
    update_canvas()

def fill_scores():
    scores.append([temp_player.score, temp_player.character_id, 100])
    for i in range(3):
        scores.append([temp_ai[i].score, temp_ai[i].ch_id, temp_ai[i].ch_id])

    # scores.append([run_track_mode.player.score, run_track_mode.player.character_id, 100])
    # for i in range(3):
    #     scores.append([run_track_mode.ai[i].score, run_track_mode.ai[i].ch_id, run_track_mode.ai[i].ch_id])

def scores_down_sort_print():
    for i in range(0, 3 + 1):
        if scores[i][2] == 1:
            character_rank_draw(temp_ai[0], i)
        elif scores[i][2] == 2:
            character_rank_draw(temp_ai[1], i)
        elif scores[i][2] == 3:
            character_rank_draw(temp_ai[2], i)
        elif scores[i][2] == 100:
            character_rank_draw(temp_player, i)
    # for i in range(0, 3 + 1):
    #     font.draw(300, 400 - 66 * i, f"{scores[i][0]:.f}", (0, 0, 0))
    #     if scores[i][2] == 0:
    #         character_rank_draw(run_track_mode.ai[0])
    #     elif scores[i][2] == 1:
    #         character_rank_draw(run_track_mode.ai[1])
    #     elif scores[i][2] == 2:
    #         character_rank_draw(run_track_mode.ai[2])
    #     elif scores[i][2] == 100:
    #         character_rank_draw(run_track_mode.player)


def character_rank_draw(obj, i):
    if i == 0:
        obj.x = 405
        obj.y = 460
    elif i == 1:
        obj.x = 300
        obj.y = 390
    elif i == 2:
        obj.x = 515
        obj.y = 390

def medal_draw():
    for i in range(0, 3 + 1):
        if scores[i][2] == 100:
            if i == 0:
                effect_image.clip_draw(27, 3683, 101, 68, 400, 550, 100, 100)
            elif i == 1:
                effect_image.clip_draw(179, 3683, 101, 68, 300, 480, 100, 100)
            elif i == 2:
                effect_image.clip_draw(331, 3683, 101, 68, 515, 480, 100, 100)
    font.draw(230, 100, f'final score: {temp_player.score}', (0, 0, 255))

def delete_object():
    global temp_player
    temp_ai[0].delete_ai()
    for i in range(3):
        game_world.remove_object(temp_ai[i])
    for i in range(3):
        del temp_ai[0]
    game_world.remove_object(temp_player)
    temp_player = None
    del temp_player
