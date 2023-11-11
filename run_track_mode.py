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
    global line_image
    global arrow_image
    global obstacle_image
    global command
    track_image = load_image('image/running_track.png')
    line_image = load_image('image/finishline.png')
    arrow_image = load_image('image/arrow.png')
    obstacle_image = load_image('image/obstacle.png')
    command = []

    running = True
    player = Player(character_select_mode.character_num)
    # player = Player(0)
    ai = [AI(player) for _ in range(3)]
    game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)


def finish():
    global track_image
    global line_image
    global arrow_image
    global obstacle_image
    del track_image
    del line_image
    del arrow_image
    del obstacle_image
    game_world.clear()


def update():
    track_update()
    game_world.update()


def draw():
    clear_canvas()
    running_track_draw()
    game_world.render()
    update_canvas()


def running_track_draw():
    global player

    for i in range(0, 21):
        track_image.clip_draw(26, 126, 254, 100, 254 * i - player.camera_x, 200, 254, 500)
        track_image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - player.camera_x, 500, 1024, 200)

    line_image.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 200 - player.camera_x, 190, 250,
                                   100)
    line_image.clip_composite_draw(0, 365, 840, 130, math.pi / 2, '', 5000 - player.camera_x, 190, 250,
                                   100)
    for i in range(1000, 5000 - 1, 500):
        for j in range(0, 4):
            obstacle_image.draw(i - player.camera_x, 120 + 50 * j + j * 10, 100, 100)
    arrow_draw()


def arrow_draw():
    global player
    for i in range(0, len(command)):
        if command[i] == 0:
            arrow_image.clip_composite_draw(0, 0, 670, 373, 0, ' ',
                                            player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)
        elif command[i] == 1:
            arrow_image.clip_composite_draw(0, 0, 670, 373, 0, 'h',
                                            player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)
        elif command[i] == 2:
            arrow_image.clip_composite_draw(0, 0, 670, 373, math.pi / 2, '',
                                            player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)
        elif command[i] == 3:
            arrow_image.clip_composite_draw(0, 0, 670, 373, math.pi / 2, 'h',
                                            player.x + i * 100 - 50 - player.camera_x,
                                            player.y + 100, 100, 100)


def track_update():
    global command
    if player.x + 100 > player.exceed_point and player.success == False:
        if len(command) == 0:
            command = [random.randint(0, 3) for n in
                            range(random.randint(3, 3))]
        elif player.x < player.exceed_point - 100:
            command.clear()
            player.input_command.clear()
            player.success = False
            player.perfect = True

        if (len(command) != 0 and len(player.input_command) != 0):
            if command[0] == player.input_command[0] and player.perfect:
                del command[0]
                player.input_command.clear()
            else:
                player.perfect = False
            if len(command) == 0 and player.perfect == True:
                player.success = True
