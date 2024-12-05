from PIL import Image, ImageDraw, ImageFont
import time
import random
from player import Player
from obstacle import Obstacle
from item import HealItem, ShieldItem, SpeedItem, ScoreItem
from util import collision_check, show_start_screen, pastel_colors
from Joystick import Joystick


def main():
    joystick = Joystick()  # 조이스틱 초기화
    width, height = joystick.width, joystick.height

    current_color_index = 0  # 현재 색의 인덱스 (초기 색상은 흰색)
    game_over = False  # 게임 오버 상태 추적 변수
    game_started = False  # 게임 시작 여부 추적 변수

    show_start_screen(joystick)  # 시작 화면 표시

    last_color_change_time = time.time()  # 마지막 색 변경 시간
    game_started = True

    while True:
        if not game_over:

            player = Player(width, height)
            obstacles = []
            heal_items = []
            shield_items = []
            speed_items = []
            score_items = []  # 스코어 아이템 리스트

            score = 0
            last_score_time = time.time()
            last_difficulty_increase_time = time.time()
            game_start_time = time.time()  # 본게임 시작 시점 저장
            last_score_item_spawn_time = game_start_time

            obstacle_speed = 5
            item_speed = 3
            obstacle_spawn_rate = 1 / 50

            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

            while player.hp > 0:
                # 배경색 변경
                if game_started and time.time() - last_color_change_time >= 31:
                    current_color_index = (current_color_index + 1) % len(pastel_colors)
                    last_color_change_time = time.time()
                background_color = pastel_colors[current_color_index]

                # 사용자 입력 처리
                command = {'left_pressed': False, 'right_pressed': False, 'jump_pressed': False}
                if not joystick.button_L.value:
                    command['left_pressed'] = True
                if not joystick.button_R.value:
                    command['right_pressed'] = True
                if not joystick.button_A.value:
                    if not player.is_jumping:
                        player.is_jumping = True
                        player.jump_start_time = time.time()

                # 플레이어 상태 업데이트
                player.move(command)
                player.jump()
                player.update_state()

                # 장애물 생성
                if random.random() < obstacle_spawn_rate:
                    obstacles.append(Obstacle(width, obstacle_speed))

                # 아이템 생성
                if time.time() - game_start_time >= 20:  # 본게임 시작 후 20초부터
                    if random.randint(1, 300) == 1:
                        heal_items.append(HealItem(width, item_speed))
                    if random.randint(1, 300) == 1:
                        shield_items.append(ShieldItem(width, item_speed))
                    if random.randint(1, 300) == 1:
                        speed_items.append(SpeedItem(width, item_speed))
                    if time.time() - last_score_item_spawn_time >= 10:
                        score_items.append(ScoreItem(width, item_speed))
                        last_score_item_spawn_time = time.time()

                # 게임 객체 이동 및 충돌 처리
                for obstacle in obstacles[:]:
                    obstacle.move()
                    if obstacle.is_out_of_bounds(height):
                        obstacles.remove(obstacle)
                    elif collision_check(player, obstacle):
                        if player.current_state == "shielded":
                            player.reset_to_base()
                        else:
                            player.change_state("hit", "player_raspi_hit.png", 0.5)
                            player.hp -= 1
                        obstacles.remove(obstacle)

                for item_list, item_class in [(heal_items, HealItem), (shield_items, ShieldItem),
                                              (speed_items, SpeedItem), (score_items, ScoreItem)]:
                    for item in item_list[:]:
                        item.move()
                        if item.is_out_of_bounds(height):
                            item_list.remove(item)
                        elif collision_check(player, item):
                            score = item.apply_effect(player, score)
                            item_list.remove(item)

                # 난이도 상승
                if time.time() - last_difficulty_increase_time >= 15:
                    obstacle_spawn_rate = min(obstacle_spawn_rate + 1 / 100, 1)
                    last_difficulty_increase_time = time.time()

                if time.time() - last_score_time >= 1:
                    score += 10
                    last_score_time = time.time()
                    obstacle_speed = min(obstacle_speed + 0.1, 15)
                    item_speed = min(item_speed + 0.05, 10)

                # 화면 그리기
                image = Image.new("RGB", (width, height), background_color)
                draw = ImageDraw.Draw(image)

                image.paste(player.player_image, tuple(player.position[:2]), mask=player.player_image)

                for obj_list in [obstacles, heal_items, shield_items, speed_items, score_items]:
                    for obj in obj_list:
                        image.paste(obj.image, tuple(obj.position[:2]), mask=obj.image)

                draw.text((10, 10), f"Score: {score}", font=font, fill="black")
                draw.text((10, 40), f"HP: {player.hp}/{player.max_hp}", font=font, fill="black")

                joystick.disp.image(image)

            # 게임 오버 상태 처리
            game_over = True
            image = Image.new("RGB", (width, height), "black")
            draw = ImageDraw.Draw(image)
            draw.text((width // 2 - 70, height // 2 - 20), "GAME OVER", font=font, fill="red")
            draw.text((width // 2 - 90, height // 2 + 10), f"Final Score: {score}", font=font, fill="white")
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
            draw.text((width // 2 - 80, height // 2 + 40), "Press A to Restart", font=small_font, fill="white")
            joystick.disp.image(image)

        # 게임 재시작 대기
        while joystick.button_A.value:
            time.sleep(0.1)
        while not joystick.button_A.value:
            time.sleep(0.1)

        # 게임 초기화
        game_over = False
        current_color_index = 0
        last_color_change_time = time.time()


if __name__ == "__main__":
    main()