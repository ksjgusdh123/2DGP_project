from pico2d import open_canvas, close_canvas
import game_framework
import character_select_mode as start_mode

open_canvas()
game_framework.run(start_mode)
close_canvas()