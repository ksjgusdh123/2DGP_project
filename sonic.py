from pico2d import *

import game_world
from clock import Running_track, Clock
from player import Player
from AI_player import AI

HEIGHT = 600

def menu():
    global character_num
    global running
    image = load_image('image/banner.png')
    while True and running:
        clear_canvas()
        image.clip_draw(584, 1202, 288, 72, 400, 525, 800, 150)
        image.clip_draw(875, 1202, 288, 72, 400, 375, 800, 150)
        image.clip_draw(2, 1052, 288, 72, 400, 225, 800, 150)
        image.clip_draw(2, 1127, 288, 72, 400, 75, 800, 150)
        update_canvas()
        if character_num != None:
            break
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                running = False
            elif event.type == SDL_MOUSEBUTTONDOWN:
                if HEIGHT - event.y < 150:
                    character_num = 3
                elif HEIGHT - event.y < 300 and HEIGHT - event.y > 150:
                    character_num = 2
                elif HEIGHT - event.y < 450 and HEIGHT - event.y > 300:
                    character_num = 1
                elif HEIGHT - event.y < 600 and HEIGHT - event.y > 450:
                    character_num = 0




def handle_event():
    global running
    global character_num

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

def init():
    global running
    global player
    global ai
    global running_track
    global character_num
    character_num = None
    running = True
    menu()
    player = Player(character_num)
    ai = [AI(player) for i in range(3)]
    running_track = Running_track(player)
    game_world.add_object(running_track, 0)
    game_world.add_objects(ai, 1)
    game_world.add_object(player, 1)

open_canvas()

init()



while running:
    handle_event()
    game_world.update()
    clear_canvas()
    game_world.render()
    update_canvas()
    delay(0.05)

close_canvas()