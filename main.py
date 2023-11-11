import pico2d
import character_select_mode

pico2d.open_canvas()
character_select_mode.init()
while character_select_mode.running:
    character_select_mode.handle_event()
    character_select_mode.update()
    character_select_mode.draw()
    pico2d.delay(0.05)
character_select_mode.finish()
pico2d.close_canvas()