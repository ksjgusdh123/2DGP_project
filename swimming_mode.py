import random

from pico2d import *
import game_framework
import character_select_mode
import game_world
from player import Player
from AI_player import AI


def handle_events():
    global running
    global character_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
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
    global command
    global command_timer
    track_image = load_image('image/swimming_track.png')
    people_image = load_image('image/running_track.png')
    rectangle_image = load_image('image/rectangle.png')
    arrow_image = load_image('image/arrow.png')

    command = []
    command_timer = []

    running = True
    player = Player(character_select_mode.character_num)
    player = Player(3)
    ai = [AI(player) for _ in range(3)]
    game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)
    player.y = 100
    ai[0].y = 400
    ai[1].y = 300
    ai[2].y = 200
    player.game_mode = 'swim'
    for i in range(0, 3):
        ai[i].y = 400 - i * 100
        ai[i].mode = 'swim'


def finish():
    global track_image
    del track_image


def update():
    track_update()
    game_world.update()


def draw():
    clear_canvas()
    draw_swimming_track()
    game_world.render()
    update_canvas()


def draw_swimming_track():
    track_image.clip_composite_draw(0, 650, 870, 1300, math.pi / 2, '', 250 - player.camera_x, 205, 400, 500)
    for i in range(1, 20 + 1):
        track_image.clip_composite_draw(0, 400, 870, 550, math.pi / 2, '', 500 * i - player.camera_x, 205, 400, 500)
        people_image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - player.camera_x, 500, 1024, 200)
    track_image.clip_composite_draw(0, 0, 870, 300, math.pi / 2, '', 5100 - player.camera_x, 205, 400, 300)
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
        rectangle_image.draw(player.x + i * 100 - 50 - player.camera_x, player.y + 100, 100 * command_timer[i] / 10, 100 * command_timer[i] / 10)

def track_update():
    global command
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
            player.speed += 0.01 * (10 - command_timer[0])
            player.input_command.clear()
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

