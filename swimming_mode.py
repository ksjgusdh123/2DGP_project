import random

from pico2d import *
import game_framework
import character_select_mode
import game_world
import middle_result_mode
import run_track_mode
import select_level_mode
import select_menu_mode
from clock import Clock
from player import Player
from AI_player import AI

player = None
ai = [None, None, None]
level = {'easy': 2, 'normal': 3, 'hard': 4}

def handle_events():
    global running
    global character_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_menu_mode)
            delete_object()
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
    global people_image
    global arrow_image
    global rectangle_image
    global red_rectangle_image
    global command
    global command_timer
    global clock
    global font
    global finish_game
    global show_result_mode
    font = load_font('font/ENCR10B.TTF', 50)
    track_image = load_image('image/swimming_track.png')
    people_image = load_image('image/running_track.png')
    rectangle_image = load_image('image/rectangle.png')
    red_rectangle_image = load_image('image/red_rectangle1.png')
    arrow_image = load_image('image/arrow.png')
    middle_result_mode.now_map = 'Swim'

    command = []
    command_timer = []
    clock = Clock()
    game_world.add_object(clock, 0)
    running = True
    finish_game = [False, False, False, False]
    show_result_mode = False
    if not select_menu_mode.game_map == 'All':
        player = Player(character_select_mode.character_num)
        ai = [AI(player) for _ in range(3)]
        game_world.add_objects(ai, 1)
        game_world.add_object(player, 1)
        basic_player_init(player)
        for i in range(0, 3):
            ai[i].y = 380 - 100 * i
            ai[i].x = 100
            ai[i].mode = 'swim'
    else:
        player = run_track_mode.player
        basic_player_init(player)
        for i in range(3):
            ai[i] = run_track_mode.ai[i]
            ai[i].mode = 'swim'
            ai[i].y = 380 - 100 * i
            ai[i].x = 100
            ai[i].finish = False
def basic_player_init(player):
    player.y = 80
    player.x = 100
    player.start = False
    player.ready = False
    player.camera_x = 0
    player.speed = 1
    player.life = 1
    player.finish = False
    player.game_mode = 'swim'

def delete_object():
    global player
    global ai
    ai[0].delete_ai()
    for i in range(3):
        game_world.remove_object(ai[i])
    for i in range(3):
        del ai[0]
    ai = [None, None, None]
    game_world.remove_object(player)
    player = None

def finish():
    global clock
    player.start = False
    player.ready = False
    if clock:
        game_world.remove_object(clock)

    # global track_image
    # del track_image
    pass

def update():
    clock_update()
    track_update()
    game_world.update()


def draw():
    clear_canvas()
    draw_swimming_track()
    game_world.render()
    rectangle_draw()
    map_timer_draw()
    update_canvas()

def map_timer_draw():
    if player.start == False:
        font.draw(300, 550, f"0:000", (0, 0, 0))
    else:
        font.draw(300, 550, f"{get_time() - player.time:.3f}", (0, 0, 0))


def draw_swimming_track():
    track_image.clip_composite_draw(0, 650, 870, 1300, math.pi / 2, '', 250 - player.camera_x, 205, 400, 500)
    for i in range(1, 20 + 1):
        track_image.clip_composite_draw(0, 400, 870, 550, math.pi / 2, '', 500 * i - player.camera_x, 205, 400, 500)
        people_image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - player.camera_x, 500, 1024, 200)
    track_image.clip_composite_draw(0, 0, 870, 300, math.pi / 2, '', 5100 - player.camera_x, 205, 400, 300)
    arrow_draw()

def result_mode_draw():
    clear_canvas()
    draw_swimming_track()
    game_world.render()


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


def rectangle_draw():
    for i in range(0, len(command)):
        if command_timer[i] <= 3 - level[select_level_mode.game_level] + 1.5:
            red_rectangle_image.draw(player.x + i * 100 - 50 - player.camera_x, player.y + 100, 100 * command_timer[i] / 10,
                                     100 * command_timer[i] / 10)
        else:
            rectangle_image.draw(player.x + i * 100 - 50 - player.camera_x, player.y + 100, 100 * command_timer[i] / 10,
                                 100 * command_timer[i] / 10)


def track_update():
    global command, show_result_mode
    global player
    global command_timer

    if len(command_timer) != 0:
        for i in range(0, len(command_timer)):
            command_timer[i] -= 0.01
            if command_timer[i] <= 0:
                player.stun = True
                command.clear()
                command_timer.clear()
                print('stun')
                break

    if player.timing_ok:
        command.append(random.randint(0, 3))
        command_timer.append(10.0)
        player.timing_ok = False

    if len(command) == 0 and len(player.input_command) != 0:
        player.input_command.clear()

    if len(command) != 0 and len(player.input_command) != 0:
        if command[0] == player.input_command[0]:
            if command_timer[0] <= 3 - level[select_level_mode.game_level] + 1.5:
                player.speed += 0.01 * ((10 - 2 * level[select_level_mode.game_level]) - command_timer[0])
            else:
                if player.speed > 1:
                    player.speed = 1
                else:
                    player.life -= 0.3
                    if player.life <= 0:
                        player.stun = True
                        command.clear()
                        command_timer.clear()
                        print('stun')
                    else:
                        player.speed = player.life
            player.input_command.clear()
            if len(command) >= 1:
                del command_timer[0]
                del command[0]
        elif command[0] != player.input_command[0]:
            player.input_command.clear()
            player.life -= 0.3
            if player.life <= 0:
                player.stun = True
                command.clear()
                command_timer.clear()
                print('stun')
            else:
                player.speed = player.life

    finish_num = 0
    for i in range(4):
        if finish_game[i]:
            finish_num += 1
    if finish_num == 4:
        show_result_mode = True

    if player.finish and finish_game[0] == False:
        finish_game[0] = True
    for i in range(3):
        if ai[i].finish and finish_game[i + 1] == False:
            finish_game[i + 1] = True

    if player.x >= 5000:
        command.clear()
        command_timer.clear()

    if show_result_mode:
        middle_result_mode.map_num += 1
        game_framework.change_mode(middle_result_mode)
        if select_menu_mode.game_map == 'All':
            player.next_map = 'long-jump'

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
