from pico2d import *

sonic_run = [7, 31, 56, 82, 105, 130, 154, 180]
sonic_slip = [4, 68, 95, 35]
sonic_jump = [6, 34, 55, 84, 109, 137, 165, 193, 219, 246]
sonic_jump_w = [21, 19, 24, 19, 25, 25, 23, 24, 24, 26]

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


def time_out(e):
    return e[0] == 'TIME_OUT'


def go_jump(e):
    return e[0] == 'JUMP'

def fail_out(e):
    return e[0] == 'FAIL'

class Idle:
    @staticmethod
    def enter(player, e):
        player.frame = 0
        player.action = 1
        pass
    @staticmethod
    def exit(player, e):
        pass
    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 10
    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame // 2 * 22 + 5, 249, 18, 30, player.x - player.camera_x, player.y, 50, 100)

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
        if get_time() - player.wait_time < 0.4:
            player.y += 10
        elif get_time() - player.wait_time > 0.4 and get_time() - player.wait_time < 0.8:
            player.y -= 10
        if get_time() - player.wait_time > 0.8:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        player.image.clip_draw(sonic_slip[player.frame // 4], 5, 28, 30, player.x - player.camera_x, player.y, 50, 100)

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
        if get_time() - player.wait_time < 0.4:
            player.y += 10
        elif get_time() - player.wait_time > 0.4 and get_time() - player.wait_time < 0.8:
            player.y -= 10
        if get_time() - player.wait_time > 0.8:
            player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        player.image.clip_draw(sonic_jump[player.frame], 215, sonic_jump_w[player.frame], 30,
                               player.x - player.camera_x, player.y, 50, 100)


class Run:
    @staticmethod
    def enter(player, e):
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
        player.frame = (player.frame + 1) % 8
        player.x += player.dir * 5

        if player.x >= 400:
            player.camera_x += player.dir * 5

        if player.x >= player.exceed_point and player.success == True:
            player.state_machine.handle_event(('JUMP', 0))
            player.exceed_point += 500
        elif player.x >= player.exceed_point and player.success == False:
            player.state_machine.handle_event(('FAIL', 0))

    @staticmethod
    def draw(player):
        if player.dir > 0:
            player.image.clip_draw(sonic_run[player.frame], 149, 23, 27, player.x - player.camera_x, player.y, 50, 100)
        elif player.dir < 0:
            player.image.clip_composite_draw(sonic_run[player.frame], 149, 23, 27, 0, 'h', player.x - player.camera_x,
                                             player.y, 50, 100)
class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {a_down: Run, d_down: Run, left_down: Run, right_down: Run, down_down: Run, up_down: Run},
            Run: {a_down: Run, d_down: Run, a_up: Idle, d_up: Idle, left_down: Run, right_down: Run, fail_out: Slip,
                  down_down: Run, up_down: Run, go_jump: Jump},
            Slip: {time_out: Idle},
            Jump: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
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
    def __init__(self):
        self.image = load_image('sonic_animation.png')
        self.frame = 0
        self.action = 1
        self.dir = 0
        self.x, self.y = 100, 140
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.camera_x = 0
        self.input_command = []
        self.success = False
        self.exceed_point = 250

    def update(self):
        self.state_machine.update()
    def handle_event(self,event):
        self.state_machine.handle_event(('INPUT', event))
        pass
    def draw(self):
        self.state_machine.draw()