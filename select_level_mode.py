from pico2d import *

import character_select_mode
import game_framework

import select_menu_mode

HEIGHT = 600
picture_size = 75
pictogram_start_x = 350
game_level = None
def handle_events():
    global running
    global game_level
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(select_menu_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if 550 <= event.x <= 745:
                if 70 <= HEIGHT - event.y <= 130:
                    game_level = 'hard'
                elif 220 <= HEIGHT - event.y <= 280:
                    game_level = 'normal'
                elif 370 <= HEIGHT - event.y <= 430:
                    game_level = 'easy'
                if not game_level is None:
                    game_framework.change_mode(character_select_mode)

def init():
    global main_background_image
    global sports_pictogram
    global run_screenshot
    global swim_screenshot
    global long_jump_screenshot
    global shooting_screenshot
    global level_box
    global running
    global font
    global mini_font
    main_background_image = load_image('image/main_background.png')
    sports_pictogram = load_image('image/pictogram.png')
    level_box = load_image('image/rectangle.png')
    run_screenshot = load_image('image/run_screen_shot.png')
    swim_screenshot = load_image('image/swim_screen_shot.png')
    long_jump_screenshot = load_image('image/long_jump_screen_shot.png')
    shooting_screenshot = load_image('image/shooting_screen_shot.png')
    running = True
    font = load_font('font/ENCR10B.TTF', 50)
    mini_font = load_font('font/NanumGothic.ttf', 20)
    if select_menu_mode.game_map == None:
        select_menu_mode.game_map = 'All'
def finish():
    global main_background_image
    global sports_pictogram
    global font
    del font
    del main_background_image
    del sports_pictogram

def update():
    pass


def draw():
    clear_canvas()
    draw_UI()
    update_canvas()


def draw_UI():
    main_background_image.clip_draw(510, 620, 90, 350, 400, 300, 800, 600)
    if select_menu_mode.game_map == 'All':
        sports_pictogram.clip_draw(0, 260, 65, 65, pictogram_start_x - 50, 550, picture_size, picture_size)
        font.draw(400, 550, f'All', (0, 0, 0))
        mini_font.draw(50, 140, f'      모든 종목을 플레이하여 종합우승 하자!', (0, 0, 0))
    elif select_menu_mode.game_map == 'hurdle race':
        sports_pictogram.clip_draw(260, 65, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        run_screenshot.draw(250, 350, 400, 200)
        font.draw(300, 550, f'hurdle race', (0, 0, 0))
        mini_font.draw(50, 220, f'd: 달리기 shift: 가속', (0, 0, 0))
        mini_font.draw(50, 200, f'장애물 주변에 접근시 커맨드 생성', (0, 0, 0))
        mini_font.draw(50, 180, f'방향키를 이용해 옳바른 커맨드를 입력', (0, 0, 0))
        mini_font.draw(50, 160, f'커맨드를 틀리거나 입력하지 못하고 달릴 시', (0, 0, 0))
        mini_font.draw(50, 140, f'넘어지면 커맨드 초기화', (0, 0, 0))
        mini_font.draw(50, 120, f'커맨드 틀릴 시에 넘어지기 전까지', (0, 0, 0))
        mini_font.draw(50, 100, f'더이상의 입력은 불가능하다', (0, 0, 0))
        mini_font.draw(50, 80, f'난이도가 올라갈 수 록 커맨드 수 증가', (0, 0, 0))
        mini_font.draw(50, 60, f'뒤로가는 키 없음!', (0, 0, 0))
    elif select_menu_mode.game_map == 'swimming':
        sports_pictogram.clip_draw(260, 260, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        swim_screenshot.draw(250, 350, 400, 200)
        font.draw(300, 550, f'swimming', (0, 0, 0))
        mini_font.draw(50, 220, f'f: 화살표 클릭', (0, 0, 0))
        mini_font.draw(50, 200, f'타이밍에 맞추어 키입력을 성공시키자', (0, 0, 0))
        mini_font.draw(50, 180, f'색깔별로 추가 속도 부여', (0, 0, 0))
        mini_font.draw(50, 160, f'검은색을 맞출 시 스턴에 빠짐', (0, 0, 0))
        mini_font.draw(50, 140, f'화살표가 왕복할 때까지 키입력이 없으면', (0, 0, 0))
        mini_font.draw(50, 120, f'스턴상태에 빠짐', (0, 0, 0))
        mini_font.draw(50, 100, f'난이도가 올라갈 수 록 화살표의 속도가 증가', (0, 0, 0))
    elif select_menu_mode.game_map == 'long-jump':
        sports_pictogram.clip_draw(0, 65, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        long_jump_screenshot.draw(250, 350, 400, 200)
        font.draw(300, 550, f'long-jump', (0, 0, 0))
        mini_font.draw(50, 220, f'd: 속도 증가 f: 달리기 정지 r: 점프 ', (0, 0, 0))
        mini_font.draw(50, 200, f'd키를 연타해 최고 속도로 달려', (0, 0, 0))
        mini_font.draw(50, 180, f'멀리 점프하자', (0, 0, 0))
        mini_font.draw(50, 160, f'점프선을 넘을 시 실격 처리', (0, 0, 0))
        mini_font.draw(50, 140, f'총 2회 점프해 높은 점수를 최종점수로', (0, 0, 0))
        mini_font.draw(50, 120, f'난이도가 올라갈 수 록 각도의 회전속도 증가', (0, 0, 0))
    elif select_menu_mode.game_map == 'shooting':
        sports_pictogram.clip_draw(130, 130, 65, 65, pictogram_start_x - 150, 550, picture_size, picture_size)
        shooting_screenshot.draw(250, 350, 400, 200)
        font.draw(300, 550, f'shooting', (0, 0, 0))
        mini_font.draw(50, 220, f'r: 발사', (0, 0, 0))
        mini_font.draw(50, 200, f'방향키로 조준점 변경', (0, 0, 0))
        mini_font.draw(50, 180, f'방향키로 장애물이 지나는 곳을 조준해 맞추자', (0, 0, 0))
        mini_font.draw(50, 160, f'장애물이 사각형에 한번도 통과하지 않을 시에', (0, 0, 0))
        mini_font.draw(50, 140, f'사격을 멈추자', (0, 0, 0))
        mini_font.draw(50, 120, f'점수가 가장 높으면 우승', (0, 0, 0))
        mini_font.draw(50, 100, f'점수가 같다면 남은 총알의 개수로 승리를 판단', (0, 0, 0))
        mini_font.draw(50, 80, f'난이도가 올라갈 수록 클레이의 속도 증가', (0, 0, 0))
    level_box.draw(250, 130, 600, 300)

    level_box.draw(650, 400, 250, 70)
    level_box.draw(650, 250, 250, 70)
    level_box.draw(650, 100, 250, 70)
    font.draw(590, 100, f'hard', (0, 0, 0))
    font.draw(565, 250, f'normal', (0, 0, 0))
    font.draw(590, 400, f'easy', (0, 0, 0))





