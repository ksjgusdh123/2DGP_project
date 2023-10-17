from pico2d import *

sonic_run = [7, 31, 56, 82, 105, 130, 154, 180]

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


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

class Run:
    @staticmethod
    def enter(player, e):
        if d_down(e):
            player.dir, player.action = 1, 1
        elif a_down(e):
            player.dir, player.action = -1, 0
        pass
    @staticmethod
    def exit(player, e):
        pass
    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 8
        player.x += player.dir * 5

        if player.x >= 400:
            player.camera_x += player.dir * 5

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
            Idle: {a_down: Run, d_down: Run, a_up: Idle, d_up: Idle},
            Run: {a_down: Idle, d_down: Idle, a_up: Idle, d_up: Idle}
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

    def update(self):
        self.state_machine.update()
    def handle_event(self,event):
        self.state_machine.handle_event(('INPUT', event))
        pass
    def draw(self):
        self.state_machine.draw()