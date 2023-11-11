from pico2d import *

import game_world
from character_sprite import *
from field import Clock


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def shift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and (e[1].key == SDLK_LSHIFT or e[1].key == SDLK_RSHIFT)

def shift_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and (e[1].key == SDLK_LSHIFT or e[1].key == SDLK_RSHIFT)

def game_start(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'


def go_jump(e):
    return e[0] == 'JUMP'

def fail_out(e):
    return e[0] == 'FAIL'


class Idle:
    @staticmethod
    def enter(player, e):
        if game_start(e):
            player.start_clock()
        player.shift = False
        player.frame = 0
        if player.action == 0:
            player.action = 2
        elif player.action == 1:
            player.action = 3
    @staticmethod
    def exit(player, e):
        player.dir = 0
    @staticmethod
    def do(player):
        if player.character_id == 1:
            player.frame = (player.frame + 1) % 14
        else:
            player.frame = (player.frame + 1) % 10
    @staticmethod
    def draw(player):
        if player.action == 3:
            if player.character_id == 0:
                player.image.clip_draw(player.frame // 2 * 22 + 5, 249, 18, 30, player.x - player.camera_x, player.y, 50, 100)
            elif player.character_id == 1:
                player.image.clip_draw(player.frame // 2 * 32 + 107, 960, 21, 35, player.x - player.camera_x, player.y, 50, 100)
            elif player.character_id == 2:
                player.image.clip_draw(player.frame // 2 * 26 + 6, 467, 23, 33, player.x - player.camera_x, player.y, 50, 100)
            elif player.character_id == 3:
                player.image.clip_draw(player.frame // 2 * 31 + 117, 262, 29, 42, player.x - player.camera_x, player.y, 50, 100)
        else:
            player.image.clip_composite_draw(player.frame // 2 * 22 + 5, 249, 18, 30, 0, 'h',
                                             player.x - player.camera_x, player.y, 50, 100)


class Slip:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.wait_time = get_time()

    @staticmethod
    def exit(player, e):
        player.success = False

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 16
        player.x -= 8
        if player.x >= 400:
            player.camera_x -= player.dir * 8
        if get_time() - player.wait_time < 0.4:
            player.y += 10
        elif get_time() - player.wait_time > 0.4 and get_time() - player.wait_time < 0.8:
            player.y -= 10
        if get_time() - player.wait_time > 0.8:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.character_id == 0:
            player.image.clip_draw(sonic_slip[player.frame // 4], 5, 28, 30, player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 1:
            player.image.clip_draw(tails_slip[player.frame // 4], 480, 30, 31, player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 2:
            player.image.clip_draw(shadow_slip[player.frame // 4], 319, 32, 32, player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 3:
            player.image.clip_draw(ech_slip[player.frame // 4], 3, 35, 41, player.x - player.camera_x, player.y, 50, 100)

class Jump:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.wait_time = get_time()

    @staticmethod
    def exit(player, e):
        player.success = False
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 10
        player.x += 8
        if player.x >= 400:
            player.camera_x += player.dir * 8
        if get_time() - player.wait_time < 0.4:
            player.y += 10
        elif get_time() - player.wait_time > 0.4 and get_time() - player.wait_time < 0.8:
            player.y -= 10
        if get_time() - player.wait_time > 0.8:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.character_id == 0:
            player.image.clip_draw(sonic_jump[player.frame], 215, sonic_jump_w[player.frame], 30,
                                   player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 1:
            player.image.clip_draw(tails_jump[player.frame], 736, tails_jump_w[player.frame], 32,
                                 player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 2:
            player.image.clip_draw(shadow_jump[player.frame], 317, shadow_jump_w[player.frame], 39,
                                 player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 3:
            player.image.clip_draw(ech_jump[player.frame], 214, ech_jump_w[player.frame], 45,
                                 player.x - player.camera_x, player.y, 50, 100)


class Run:
    @staticmethod
    def enter(player, e):
        if shift_down(e):
            player.shift = True
            player.wait_time = get_time()
        elif shift_up(e):
            player.shift = False

        if d_down(e):
            player.dir, player.action = 1, 1
        elif a_down(e):
            player.dir, player.action = -1, 0

        if left_down(e):
            player.input_command.insert(0, 0)
        elif right_down(e):
            player.input_command.insert(0, 1)
        elif down_down(e):
            player.input_command.insert(0, 2)
        elif up_down(e):
            player.input_command.insert(0, 3)
    @staticmethod
    def exit(player, e):
        if left_down(e):
            player.input_command.insert(0, 0)
        elif right_down(e):
            player.input_command.insert(0, 1)
        elif down_down(e):
            player.input_command.insert(0, 2)
        elif up_down(e):
            player.input_command.insert(0, 3)
    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 10

        if player.shift and player.dir != 0:
            add_speed = get_time() - player.wait_time
            if player.x <= 5150:
                player.x += (player.dir + min(add_speed, 1)) * 5
            if player.x >= 400 and player.x <= 4800:
                player.camera_x += (player.dir + min(add_speed, 1)) * 5
        else:
            if player.x <= 5150:
                player.x += player.dir * 5
            if player.x >= 400 and player.x <= 4800:
                player.camera_x += player.dir * 5

        if player.x >= player.exceed_point and player.success == True:
            player.state_machine.handle_event(('JUMP', 0))
            if player.exceed_point + 500 < 4600:
                player.exceed_point += 500
            else:
                player.exceed_point = 10000
        elif player.x >= player.exceed_point and player.success == False:
            player.state_machine.handle_event(('FAIL', 0))

    @staticmethod
    def draw(player):
        if player.character_id == 0:
            if player.dir > 0:
                player.image.clip_draw(sonic_run[player.frame], 149, 23, 27, player.x - player.camera_x, player.y, 50, 100)
            elif player.dir < 0:
                player.image.clip_composite_draw(sonic_run[player.frame], 149, 23, 27, 0, 'h', player.x - player.camera_x,
                                                 player.y, 50, 100)
            else:
                player.image.clip_draw(player.frame // 2 * 22 + 5, 249, 18, 30, player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 1:
            if player.dir > 0:
                player.image.clip_draw(tails_run[player.frame], 784, 36, 35, player.x - player.camera_x, player.y, 50, 100)
            elif player.dir == 0:
                player.image.clip_draw(player.frame // 2 * 32 + 107, 960, 21, 35, player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 2:
            if player.dir >0:
                player.image.clip_draw(shadow_run[player.frame], 431, shadow_run_w[player.frame], 32, player.x - player.camera_x, player.y, 50, 100)
            else:
                player.image.clip_draw(player.frame // 2 * 26 + 6, 467, 23, 33, player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 3:
            if player.dir > 0:
                player.image.clip_draw(ech_run[player.frame], 218, ech_run_w[player.frame], 40, player.x - player.camera_x, player.y, 50, 100)
            else:
                player.image.clip_draw(player.frame // 2 * 31 + 117, 262, 29, 42, player.x - player.camera_x, player.y, 50, 100)
class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {a_down: Run, d_down: Run, left_down: Run, right_down: Run, down_down: Run, up_down: Run, game_start: Idle},
            Run: {a_down: Run, d_down: Run, a_up: Idle, d_up: Idle, left_down: Run, right_down: Run, fail_out: Slip,
                  down_down: Run, up_down: Run, go_jump: Jump, shift_down: Run, shift_up: Run},
            Slip: {time_out: Idle},
            Jump: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e) and (self.player.start or game_start(e)):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True
        return False

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class Player:
    def __init__(self, character_num):
        self.character_id = character_num
        if self.character_id == 0:
            self.image = load_image('image/sonic_animation.png')
        if self.character_id == 1:
            self.image = load_image('image/tails.png')
        if self.character_id == 2:
            self.image = load_image('image/shadow.png')
        if self.character_id == 3:
            self.image = load_image('image/echidna.png')

        self.frame = 0
        self.action = 1
        self.dir = 0
        self.x, self.y = 100, 140
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.camera_x = 0
        self.start = False
        self.ready = False
        # running_track
        self.input_command = []
        self.success = False
        self.exceed_point = 950
        self.perfect = True
        self.shift = False

    def update(self):
        self.state_machine.update()
    def handle_event(self,event):
        self.state_machine.handle_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()


    def start_clock(self):
        if not self.start and not self.ready:
            clock = Clock(self)
            game_world.add_object(clock, 0)
            self.ready = True
            print('clock spone')
