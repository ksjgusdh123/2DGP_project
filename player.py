from pico2d import load_image

class Idle:
    @staticmethod
    def enter(player):
        player.frame = 0
        player.action = 1
        pass
    @staticmethod
    def exit(player):
        pass
    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 10
    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame // 2 * 22 + 5, 249, 18, 30, player.x, player.y, 50, 100)
class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle

    def start(self):
        self.cur_state.enter(self.player)

    def update(self):
        self.cur_state.do(self.player)

    def draw(self):
        self.cur_state.draw(self.player)

class Player:
    def __init__(self):
        self.image = load_image('sonic_animation.png')
        self.frame = 0
        self.action = 1
        self.x, self.y = 100, 100
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()
    def handle_event(self,event):
        pass
    def draw(self):
        self.state_machine.draw()