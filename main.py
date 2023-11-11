import pico2d
import play_mode

pico2d.open_canvas()
play_mode.init()
while play_mode.running:
    play_mode.handle_event()
    play_mode.update()
    play_mode.draw()
    pico2d.delay(0.05)
play_mode.finish()
pico2d.close_canvas()