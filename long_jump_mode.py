
from pico2d import *
import game_framework
import character_select_mode
import game_world
import middle_result_mode
import select_menu_mode
from clock import Clock
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
    global line_image
    global angle_image
    global arrow_image
    global command
    global angle
    global angle_flip
    global clock
    global jump_chance
    middle_result_mode.now_map = 'long-jump'
    track_image = load_image('image/running_track.png')
    line_image = load_image('image/finishline.png')
    angle_image = load_image('image/angle.png')
    arrow_image = load_image('image/arrow_flip.png')
    clock = Clock()
    command = []
    game_world.add_object(clock, 0)
    angle = 0
    angle_flip = False
    jump_chance = 2
    if not select_menu_mode.game_map == 'All':
        running = True
        player = Player(character_select_mode.character_num)
        # player = Player(0)
        # ai = [AI(player) for _ in range(3)]
        # game_world.add_objects(ai, 1)
        game_world.add_object(player, 1)
        player.y = 240
        player.x = 100

    player.game_mode = 'jump'

def restart():
    global clock
    clock = Clock()
    game_world.add_object(clock, 0)
    player.camera_x = 0
    player.start = False
    player.y = 240
    player.x = 100
    player.stop = False
    player.jump_ok = False
    player.jump_finish = False
    player.angle_check = False

def delete_object():
    global player
    # ai[0].delete_ai()
    # for i in range(3):
    #     game_world.remove_object(ai[i])
    game_world.remove_object(player)
    player = None

def finish():
    global clock
    player.start = False
    player.ready = False
    if clock:
        game_world.remove_object(clock)

    # global line_image
    # global arrow_image
    # global obstacle_image
    # del line_image
    # del arrow_image
    # del obstacle_image
    # game_world.clear()

def update():
    clock_update()
    long_jump_update()
    game_world.update()




def draw():
    clear_canvas()
    track_draw()
    game_world.render()
    update_canvas()


def track_draw():
    for i in range(0, 20 + 1):
        track_image.clip_draw(26, 126, 254, 100, 254 * i - player.camera_x, 200, 254, 500)
        track_image.clip_draw(28, 236, 208, 64, 1024 * (i // 4) - player.camera_x, 500, 1024, 200)
    track_image.clip_draw(396, 442, 92, 50, 2000 - player.camera_x, 190, 1000, 254)

    if player.stop:
        arrow_image.clip_composite_draw(-100, 0, 620, 373, angle * math.pi / 180.0, '', player.x + 100 - 60 - player.camera_x - angle * 0.25,
                                        player.y + 80 - (90 - angle) * 0.1, 100, 50)
        angle_image.draw(player.x + 100 - 50 - player.camera_x, player.y + 100, 100, 100)


def clock_update():
    global clock
    if not clock is None:
        if clock.interval >= 3:
            player.start = True
            player.time = get_time()
            # for i in range(0, 3):
            #     ai[i].time = player.time
            game_world.remove_object(clock)
            clock = None

def long_jump_update():
    global player
    global angle
    global angle_flip

    if player.jump_finish and jump_chance > 0:
        restart()
        jump_chance -= 1

    if player.stop:
        if angle_flip:
            angle -= 0.1
        else:
            angle += 0.1
        if angle >= 90:
            angle = 90
            angle_flip = True
        if angle <= 0:
            angle = 0
            angle_flip = False
    if player.angle_check:
        player.angle = angle * math.pi / 180.0
        player.angle_check = False
        player.stop = False
        print(angle)
