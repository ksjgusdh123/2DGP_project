import random

from pico2d import *
import game_framework
import character_select_mode
import game_world
import middle_result_mode
import select_level_mode
import select_menu_mode
import swimming_mode
from clock import Clock
from player import Player
from AI_player import AI

level = {'easy': 2, 'normal': 3, 'hard': 4}
player = None
ai = [None, None, None]
def handle_events():
    global running
    global character_num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(character_select_mode)
            delete_object()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.change_mode(swimming_mode)
        elif not clock is None and event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            player.ready = True
            clock.start = True
            print('clock spone')
        else:
            player.handle_event(event)


def init():
    global running
    global player
    global ai
    global track_image
    global line_image
    global arrow_image
    global obstacle_image
    global command
    global clock
    global font
    global finish_game
    global show_result_mode
    middle_result_mode.now_map = 'Run'
    track_image = load_image('image/running_track.png')
    line_image = load_image('image/finishline.png')
    arrow_image = load_image('image/arrow.png')
    obstacle_image = load_image('image/obstacle.png')
    font = load_font('font/ENCR10B.TTF', 50)

    command = []

    running = True
    player = Player(character_select_mode.character_num)
    # player = Player(0)
    ai = [AI(player) for _ in range(3)]
    clock = Clock()
    game_world.add_object(clock, 0)
    game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)
    basic_player_init(player)
    for i in range(0, 3):
        ai[i].x = 100
        ai[i].y = 320 - 60 * i
        ai[i].mode = 'run'
    if select_level_mode.game_level is None:
        select_level_mode.game_level = 'easy'

    finish_game = [False, False, False, False]
    show_result_mode = False

def basic_player_init(player):
    player.y = 140
    player.x = 100
    player.start = False
    player.ready = False
    player.exceed_point = 950
    player.input_command = []
    player.game_mode = 'run'

def delete_object():
    global player
    global ai
    ai[0].delete_ai()
    for i in range(3):
        game_world.remove_object(ai[i])
    for i in range(3):
        del ai[0]
    game_world.remove_object(player)
    player = None
    del player

def finish():
    global clock
    player.start = False
    player.ready = False
    if clock:
        game_world.remove_object(clock)
    # global track_image
    # global line_image
    # global arrow_image
    # global obstacle_image
    # del track_image
    # del line_image
    # del arrow_image
    # del obstacle_image
    # global ai
    # ai[0].delete_ai()
    # game_world.clear()
    pass

def update():
    clock_update()
    track_update()
    game_world.update()




def draw():
    clear_canvas()
    running_track_draw()
    game_world.render()
    map_timer_draw()
    update_canvas()


def map_timer_draw():
    if player.start == False:
        font.draw(300, 550, f"0:000", (0, 0, 0))
    else:
        font.draw(300, 550, f"{get_time() - player.time:.3f}", (0, 0, 0))


def result_mode_draw():
    clear_canvas()
    running_track_draw()
    game_world.render()

def running_track_draw():
    for i in range(0, 21):
        track_image.clip_draw(26, 126, 254, 100, 254 * i - player.camera_x, 200, 254, 500)
        track_image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - player.camera_x, 500, 1024, 200)

    line_image.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 200 - player.camera_x, 190, 250, 100)
    line_image.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 5000 - player.camera_x, 190, 250, 100)
    for i in range(1000, 5000 - 1, 500):
        for j in range(0, 4):
            obstacle_image.draw(i - player.camera_x, 120 + 50 * j + j * 10, 100, 100)
    arrow_draw()


def arrow_draw():
    for i in range(0, len(command)):
        if command[i] == 0:
            arrow_image.clip_composite_draw(0, 0, 670, 373, 0, ' ', player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)
        elif command[i] == 1:
            arrow_image.clip_composite_draw(0, 0, 670, 373, 0, 'h', player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)
        elif command[i] == 2:
            arrow_image.clip_composite_draw(0, 0, 670, 373, math.pi / 2, '', player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)
        elif command[i] == 3:
            arrow_image.clip_composite_draw(0, 0, 670, 373, math.pi / 2, 'h', player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)

def clock_update():
    global clock
    if not clock is None:
        if clock.interval >= 3:
            player.start = True
            player.time = get_time()
            for i in range(0, 3):
                ai[i].time = player.time
            game_world.remove_object(clock)
            clock = None


def track_update():
    global command
    global show_result_mode
    global player
    if player.x + 100 > player.exceed_point and player.success == False:
        if len(command) == 0:
            command = [random.randint(0, 3) for _ in range(level[select_level_mode.game_level])]
    elif player.x < player.exceed_point - 100:
        command.clear()
        player.input_command.clear()
        player.success = False
        player.perfect = True

    if len(command) != 0 and len(player.input_command) != 0:
        if command[0] == player.input_command[0] and player.perfect:
            del command[0]
            player.input_command.clear()
        else:
            player.perfect = False
        if len(command) == 0 and player.perfect == True:
            player.success = True

    if player.x >= 5000:
        print(get_time() - player.time)

    if player.finish and finish_game[0] == False:
        finish_game[0] = True
    for i in range(3):
        if ai[i].finish and finish_game[i + 1] == False:
            finish_game[i + 1] = True

    finish_num = 0
    for i in range(4):
        if finish_game[i]:
            finish_num += 1
    if finish_num == 4:
        show_result_mode = True

    if show_result_mode:
        middle_result_mode.map_num += 1
        game_framework.change_mode(middle_result_mode)
        if select_menu_mode.game_map == 'All':
            player.next_map = 'swim'
