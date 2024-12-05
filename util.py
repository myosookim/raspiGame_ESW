from PIL import ImageChops, Image
import time

# 파스텔 색상
pastel_colors = [
    (255, 255, 255),
    (255, 182, 182),
    (255, 255, 182),
    (182, 255, 182),
    (182, 255, 255),
    (255, 182, 255)
]


def show_start_screen(joystick):
    start_image = Image.open("startscreen.png").convert("RGB")
    start_image = start_image.resize((joystick.width, joystick.height))
    joystick.disp.image(start_image)

    while True:
        if not joystick.button_A.value:
            break
        time.sleep(0.1)

    while not joystick.button_A.value:
        time.sleep(0.1)


def collision_check(player, obj):
    px1, py1, px2, py2 = player.position
    ox1, oy1, ox2, oy2 = obj.position

    if px2 < ox1 or px1 > ox2 or py2 < oy1 or py1 > oy2:
        return False

    player_bbox = player.player_image.crop((ox1 - px1, oy1 - py1, ox2 - px1, oy2 - py1))
    obj_bbox = obj.image.crop((px1 - ox1, py1 - oy1, px2 - ox1, py2 - oy1))

    player_alpha = player_bbox.getchannel("A")
    obj_alpha = obj_bbox.getchannel("A")

    overlap = ImageChops.multiply(player_alpha, obj_alpha)
    return overlap.getbbox() is not None
