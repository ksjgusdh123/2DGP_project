from pico2d import *

import game_framework
import game_world
import run_track_mode
import start_game_mode

scores = []

SONIC = 0
TAILS = 1
SHADOW = 2
ECHDNA = 3
player = None
ai = [None, None, None]
def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(start_game_mode)


def init():
    global main_background_image
    global character_result_image
    global effect_image
    global font
    global temp_player
    global temp_ai
    global ai
    global player
    global win_sound
    global lose_sound
    global else_sound
    main_background_image = load_image('image/ending_background.png')
    effect_image = load_image('image/effect.png')
    character_result_image = load_image('image/result.png')
    font = load_font('font/ENCR10B.TTF', 40)
    win_sound = load_music('sound/final_win.mp3')
    lose_sound = load_music('sound/final_lose.mp3')
    else_sound = load_music('sound/final_else.mp3')

    # temp_player = Player(0)
    # temp_ai = [AI(temp_player) for _ in range(3)]
    # game_world.add_objects(temp_ai, 1)
    # game_world.add_object(temp_player, 1)
    #
    # temp_player.score = 19
    # temp_player.game_mode = 'run'
    # for i in range(3):
    #     temp_ai[i].score = i + 2
    #     temp_ai[i].mode = 'run'
    player = run_track_mode.player
    player.camera_x = 0
    for i in range(3):
        ai[i] = run_track_mode.ai[i]
        ai[i].mode = 'run'
    fill_scores()
    scores.sort(reverse=True)
    player.sound_ok = False

def delete_object():
    global player
    global ai
    ai[0].delete_ai()
    for i in range(3):
        game_world.remove_object(ai[i])
    for i in range(3):
        del ai[0]
    game_world.remove_object(player)
    ai = [None, None, None]
    player = None
    del player


def finish():
    global scores
    scores.clear()
    delete_object()

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
    # scores.append([temp_player.score, temp_player.character_id, 100])
    # for i in range(3):
    #     scores.append([temp_ai[i].score, temp_ai[i].ch_id, temp_ai[i].ch_id])

    scores.append([player.score, player.character_id, 100])
    for i in range(3):
        scores.append([ai[i].score, ai[i].ch_id, ai[i].temp_num])

def scores_down_sort_print():
    global ai
    global player
    # for i in range(0, 3 + 1):
    #     if scores[i][2] == 1:
    #         character_rank_draw(temp_ai[0], i)
    #     elif scores[i][2] == 2:
    #         character_rank_draw(temp_ai[1], i)
    #     elif scores[i][2] == 3:
    #         character_rank_draw(temp_ai[2], i)
    #     elif scores[i][2] == 100:
    #         character_rank_draw(temp_player, i)
    for i in range(0, 3 + 1):
        if scores[i][2] == 0:
            character_rank_draw(ai[0], i)
        elif scores[i][2] == 1:
            character_rank_draw(ai[1], i)
        elif scores[i][2] == 2:
            character_rank_draw(ai[2], i)
        elif scores[i][2] == 100:
            character_rank_draw(player, i)
            if not player.sound_ok:
                if i == 0:
                    win_sound.play(1)
                elif i == 3:
                    lose_sound.play(1)
                else:
                    else_sound.play(1)
                player.sound_ok = True

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
    elif i == 3:
        obj.x = 105
        obj.y = 250

def medal_draw():
    for i in range(0, 3 + 1):
        if scores[i][2] == 100:
            if i == 0:
                effect_image.clip_draw(27, 3683, 101, 68, 400, 550, 100, 100)
            elif i == 1:
                effect_image.clip_draw(179, 3683, 101, 68, 300, 480, 100, 100)
            elif i == 2:
                effect_image.clip_draw(331, 3683, 101, 68, 515, 480, 100, 100)
    font.draw(230, 100, f'final score: {player.score}', (0, 0, 255))
