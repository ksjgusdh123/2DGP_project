from pico2d import *

import game_framework
import game_world
from character_sprite import *
from clock import Clock

PIXEL_PER_METER = 10 / 0.3
RUN_SPEED_KMPH = 20
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000 / 60
RUN_SPEED_MPS = RUN_SPEED_MPM / 60
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

SONIC = 0
TAILS = 1
SHADOW = 2
ECHDNA = 3


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


def wait_wide_jump(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f


def wide_jump_go(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r


def time_out(e):
    return e[0] == 'TIME_OUT'


def go_jump(e):
    return e[0] == 'JUMP'


def fail_out(e):
    return e[0] == 'FAIL'


def go_swim(e):
    return e[0] == 'GO_SWIM'


def wide_jump_run(e):
    return e[0] == 'WIDE_JUMP_RUN'


def stun(e):
    return e[0] == 'STUN'


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
            player.frame = (player.frame + 14 * ACTION_PER_TIME * game_framework.frame_time) % 14
        else:
            player.frame = (player.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        if player.start and player.game_mode == 'swim':
            player.state_machine.handle_event(('GO_SWIM', 0))
        if player.start and player.game_mode == 'jump':
            player.state_machine.handle_event(('WIDE_JUMP_RUN', 0))

    @staticmethod
    def draw(player):
        if player.game_mode == 'run' or player.game_mode == 'jump':
            Idle.running_track_idle_draw(player)
        elif player.game_mode == 'swim':
            Idle.running_track_idle_draw(player)

    @staticmethod
    def running_track_idle_draw(player):
        if player.action == 3:
            if player.character_id == 0:
                player.image.clip_draw(int(player.frame) // 2 * 22 + 5, 249, 18, 30, player.x - player.camera_x,
                                       player.y, 50, 100)
            elif player.character_id == 1:
                player.image.clip_draw(int(player.frame) // 2 * 32 + 107, 960, 21, 35, player.x - player.camera_x,
                                       player.y, 50, 100)
            elif player.character_id == 2:
                player.image.clip_draw(int(player.frame) // 2 * 26 + 6, 467, 23, 33, player.x - player.camera_x,
                                       player.y, 50, 100)
            elif player.character_id == 3:
                player.image.clip_draw(int(player.frame) // 2 * 31 + 117, 262, 29, 42, player.x - player.camera_x,
                                       player.y, 50, 100)


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
        player.frame = (player.frame + 16 * ACTION_PER_TIME * game_framework.frame_time) % 16
        player.x -= 1 * RUN_SPEED_PPS * game_framework.frame_time
        if player.x >= 400:
            player.camera_x -= player.dir * 1 * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - player.wait_time < 0.4:
            player.y += 1 * RUN_SPEED_PPS * game_framework.frame_time
        elif 0.4 < get_time() - player.wait_time < 0.8:
            player.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - player.wait_time > 0.8:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.character_id == 0:
            player.image.clip_draw(sonic_slip[int(player.frame) // 4], 5, 28, 30, player.x - player.camera_x, player.y,
                                   50, 100)
        elif player.character_id == 1:
            player.image.clip_draw(tails_slip[int(player.frame) // 4], 480, 30, 31, player.x - player.camera_x,
                                   player.y, 50, 100)
        elif player.character_id == 2:
            player.image.clip_draw(shadow_slip[int(player.frame) // 4], 319, 32, 32, player.x - player.camera_x,
                                   player.y, 50, 100)
        elif player.character_id == 3:
            player.image.clip_draw(ech_slip[int(player.frame) // 4], 3, 35, 41, player.x - player.camera_x, player.y,
                                   50, 100)


class Jump:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.wait_time = get_time()

    @staticmethod
    def exit(player, e):
        player.success = False

    @staticmethod
    def do(player):
        player.frame = (player.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        player.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
        if player.x >= 400:
            player.camera_x += player.dir * 1 * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - player.wait_time < 0.4:
            player.y += 1 * RUN_SPEED_PPS * game_framework.frame_time
        elif 0.4 < get_time() - player.wait_time < 0.8:
            player.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time
        if get_time() - player.wait_time > 0.8:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.character_id == 0:
            player.image.clip_draw(sonic_jump[int(player.frame)], 215, sonic_jump_w[int(player.frame)], 30,
                                   player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 1:
            player.image.clip_draw(tails_jump[int(player.frame)], 736, tails_jump_w[int(player.frame)], 32,
                                   player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 2:
            player.image.clip_draw(shadow_jump[int(player.frame)], 317, shadow_jump_w[int(player.frame)], 39,
                                   player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == 3:
            player.image.clip_draw(ech_jump[int(player.frame)], 214, ech_jump_w[int(player.frame)], 45,
                                   player.x - player.camera_x, player.y, 50, 100)


class Stun:
    @staticmethod
    def enter(player, e):
        player.wait_time = get_time()

    @staticmethod
    def exit(player, e):
        player.stun = False
        player.speed = 1
        player.life = 1

    @staticmethod
    def do(player):
        player.frame = (player.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        if get_time() - player.wait_time >= 1:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        if player.character_id == SONIC:
            player.image.clip_draw(sonic_stun[int(player.frame)], 6, 28, 31, player.x - player.camera_x, player.y - 20,
                                   50, 100)
        elif player.character_id == TAILS:
            player.image.clip_draw(tails_stun[int(player.frame)], 224, 40, 31, player.x - player.camera_x,
                                   player.y - 20, 50, 100)
        elif player.character_id == SHADOW:
            player.image.clip_draw(shadow_stun[int(player.frame)], 319, 30, 31, player.x - player.camera_x,
                                   player.y - 20, 50, 100)
        elif player.character_id == ECHDNA:
            player.image.clip_draw(ech_stun[int(player.frame)], 3, 35, 41, player.x - player.camera_x, player.y - 20,
                                   50, 100)


class Swim:
    @staticmethod
    def enter(player, e):
        player.dir, player.action = 1, 1
        player.wait_time = get_time()

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
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        if player.x <= 5150:
            player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time * player.speed
        if 400 <= player.x <= 4800:
            player.camera_x += player.dir * RUN_SPEED_PPS * game_framework.frame_time * player.speed

        if get_time() - player.wait_time >= 1:
            player.wait_time = get_time()
            player.timing_ok = True
            print('호출')

        if player.stun:
            player.state_machine.handle_event(('STUN', 0))

    @staticmethod
    def draw(player):
        if player.character_id == SONIC:
            player.image.clip_draw(sonic_swim[int(player.frame)], 57, 36, 20, player.x - player.camera_x, player.y, 50,
                                   100)
        elif player.character_id == TAILS:
            player.image.clip_composite_draw(tails_swim[int(player.frame)], 264, 40, 30, 3.14 * 30, 'h',
                                             player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == SHADOW:
            player.image.clip_composite_draw(shadow_swim[int(player.frame)], 284, 38, 30, 3.14 * 30, 'h',
                                             player.x - player.camera_x, player.y, 50, 100)
        elif player.character_id == ECHDNA:
            player.image.clip_draw(ech_swim[int(player.frame)], 51, 50, 25, player.x - player.camera_x, player.y, 50,
                                   100)


class Wait_Wide_Jump:
    @staticmethod
    def enter(player, e):
        if wait_wide_jump(e):
            player.stop = True

        if wide_jump_go(e):
            player.stop = False

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def draw(player):
        if player.character_id == SONIC:
            player.image.clip_draw(333, 149, 26, 25, player.x - player.camera_x, player.y, 50, 100)


class Wide_Jump:
    @staticmethod
    def enter(player, e):
        if wide_jump_go(e):
            player.angle_check = True
            player.wait_time = get_time()
            player.start_pos = player.x
    @staticmethod
    def exit(player, e):
        print(player.x - player.start_pos)
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 5
        player.x += (RUN_SPEED_PPS * game_framework.frame_time * player.speed * 3
                     * (math.cos(player.angle) - (1 - math.sin(player.angle))) / 2)

        if 400 <= player.x <= 4800:
            player.camera_x += (RUN_SPEED_PPS * game_framework.frame_time * player.speed * 3
                                * (math.cos(player.angle) - (1 - math.sin(player.angle))) / 2)

        if get_time() - player.wait_time < 0.5:
            player.y += RUN_SPEED_PPS * game_framework.frame_time * math.sin(player.angle) * 5
        elif 0.5 < get_time() - player.wait_time < 1.0:
            player.y -= RUN_SPEED_PPS * game_framework.frame_time * math.sin(player.angle) * 5
        if get_time() - player.wait_time > 1.0:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):

        if player.character_id == SONIC:
            player.image.clip_draw(sonic_wide_jump[int(player.frame)], 149, 26, 28, player.x - player.camera_x,
                                   player.y, 50, 100)


class Run:
    @staticmethod
    def enter(player, e):
        if player.game_mode == 'run':
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
        elif player.game_mode == 'jump':
            player.dir, player.action = 1, 1
            if d_down(e):
                player.speed += 0.1
    @staticmethod
    def exit(player, e):
        if player.game_mode == 'run':
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
        player.frame = (player.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        if player.game_mode == 'run':
            if player.shift and player.dir != 0:
                add_speed = get_time() - player.wait_time
                if player.x <= 5150:
                    player.x += (player.dir + min(add_speed, 1)) * RUN_SPEED_PPS * game_framework.frame_time
                if 400 <= player.x <= 4800:
                    player.camera_x += (player.dir + min(add_speed, 1)) * RUN_SPEED_PPS * game_framework.frame_time
            else:
                if player.x <= 5150:
                    player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
                if 400 <= player.x <= 4800:
                    player.camera_x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
            if player.x >= player.exceed_point and player.success:
                player.state_machine.handle_event(('JUMP', 0))
                if player.exceed_point + 500 < 4600:
                    player.exceed_point += 500
                else:
                    player.exceed_point = 10000
            elif player.x >= player.exceed_point and player.success == False:
                player.state_machine.handle_event(('FAIL', 0))

        elif player.game_mode == 'jump':
            player.speed -= 0.0005
            if player.x <= 5150:
                player.x += RUN_SPEED_PPS * game_framework.frame_time * max(player.speed, 0.5)
            if 400 <= player.x <= 4800:
                player.camera_x += RUN_SPEED_PPS * game_framework.frame_time * max(player.speed, 0.5)

    @staticmethod
    def draw(player):
        Run.run_track_draw(player)

    @staticmethod
    def run_track_draw(player):
        if player.character_id == 0:
            if player.dir > 0:
                player.image.clip_draw(sonic_run[int(player.frame)], 149, 23, 27, player.x - player.camera_x, player.y,
                                       50, 100)
            elif player.dir < 0:
                player.image.clip_composite_draw(sonic_run[int(player.frame)], 149, 23, 27, 0, 'h',
                                                 player.x - player.camera_x, player.y, 50, 100)
            else:
                player.image.clip_draw(int(player.frame) // 2 * 22 + 5, 249, 18, 30, player.x - player.camera_x,
                                       player.y, 50, 100)
        elif player.character_id == 1:
            if player.dir > 0:
                player.image.clip_draw(tails_run[int(player.frame)], 784, 36, 35, player.x - player.camera_x, player.y,
                                       50, 100)
            elif player.dir == 0:
                player.image.clip_draw(int(player.frame) // 2 * 32 + 107, 960, 21, 35, player.x - player.camera_x,
                                       player.y, 50, 100)
        elif player.character_id == 2:
            if player.dir > 0:
                player.image.clip_draw(shadow_run[int(player.frame)], 431, shadow_run_w[int(player.frame)], 32,
                                       player.x - player.camera_x, player.y, 50, 100)
            else:
                player.image.clip_draw(int(player.frame) // 2 * 26 + 6, 467, 23, 33, player.x - player.camera_x,
                                       player.y, 50, 100)
        elif player.character_id == 3:
            if player.dir > 0:
                player.image.clip_draw(ech_run[int(player.frame)], 218, ech_run_w[int(player.frame)], 40,
                                       player.x - player.camera_x, player.y, 50, 100)
            else:
                player.image.clip_draw(int(player.frame) // 2 * 31 + 117, 262, 29, 42, player.x - player.camera_x,
                                       player.y, 50, 100)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {a_down: Run, d_down: Run, left_down: Run, right_down: Run, down_down: Run, up_down: Run,
                   game_start: Idle, go_swim: Swim, wide_jump_run: Run},
            Run: {a_down: Run, d_down: Run, a_up: Idle, d_up: Idle, left_down: Run, right_down: Run, fail_out: Slip,
                  down_down: Run, up_down: Run, go_jump: Jump, shift_down: Run, shift_up: Run,
                  wait_wide_jump: Wait_Wide_Jump},
            Swim: {left_down: Swim, right_down: Swim, down_down: Swim, up_down: Swim, stun: Stun},
            Stun: {time_out: Swim},
            Slip: {time_out: Idle},
            Jump: {time_out: Idle},
            Wait_Wide_Jump: {wide_jump_go: Wide_Jump},
            Wide_Jump: {time_out: Idle}
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
        self.start = False
        self.ready = False
        self.game_mode = None
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.camera_x = 0
        # running_track
        self.input_command = []
        self.success = False
        self.exceed_point = 950
        self.perfect = True
        self.shift = False
        # swimming_mode
        self.timing_ok = False
        self.speed = 1  # wide_jump_mode
        self.stun = False
        self.life = 1
        # wide_jump_mode
        self.stop = False
        self.angle = 0
        self.angle_check = False

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def start_clock(self):
        if not self.start and not self.ready:
            clock = Clock(self)
            game_world.add_object(clock, 0)
            self.ready = True
            print('clock spone')
