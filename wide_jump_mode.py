
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
    global command
    track_image = load_image('image/running_track.png')
    line_image = load_image('image/finishline.png')
    command = []

    running = True
    # player = Player(character_select_mode.character_num)
    player = Player(0)
    # ai = [AI(player) for _ in range(3)]
    # game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)
    player.y = 240
    player.game_mode = 'jump'


def finish():
    global track_image
    # global line_image
    # global arrow_image
    # global obstacle_image
    del track_image
    # del line_image
    # del arrow_image
    # del obstacle_image
    # game_world.clear()


def update():
    game_world.update()


def draw():
    clear_canvas()
    for i in range(0, 20 + 1):
        track_image.clip_draw(26, 126, 254, 100, 254 * i - player.camera_x, 200, 254, 500)
        track_image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - player.camera_x, 500, 1024, 200)
    track_image.clip_draw(396, 442, 92, 50, 2000 - player.camera_x, 190, 1000, 254)
    game_world.render()
    update_canvas()
