from PIL import Image
import random
import numpy as np

# 회복 아이템
class HealItem:
    def __init__(self, width, speed):
        x = random.randint(0, width - 15)
        self.position = np.array([x, -15, x + 15, 0])
        self.speed = speed
        self.image = Image.open("healItem.png").convert("RGBA").resize((22, 22))

    def move(self):
        self.position[1] += self.speed
        self.position[3] += self.speed

    def is_out_of_bounds(self, height):
        return self.position[1] > height

    def apply_effect(self, player, score):
        if player.hp < player.max_hp:
            player.hp += 1
        return score

# 쉴드 아이템
class ShieldItem:
    def __init__(self, width, speed):
        x = random.randint(0, width - 15)
        self.position = np.array([x, -15, x + 15, 0])
        self.speed = speed
        self.image = Image.open("shieldItem.png").convert("RGBA").resize((30, 30))

    def move(self):
        self.position[1] += self.speed
        self.position[3] += self.speed

    def is_out_of_bounds(self, height):
        return self.position[1] > height

    def apply_effect(self, player, score):
        player.change_state("shielded", "player_raspi_shielded.png", 3)
        return score

# 속도 아이템
class SpeedItem:
    def __init__(self, width, speed):
        x = random.randint(0, width - 15)
        self.position = np.array([x, -15, x + 15, 0])
        self.speed = speed
        self.image = Image.open("speedItem.png").convert("RGBA").resize((30, 30))

    def move(self):
        self.position[1] += self.speed
        self.position[3] += self.speed

    def is_out_of_bounds(self, height):
        return self.position[1] > height

    def apply_effect(self, player, score):
        player.change_state("fast", "player_raspi_fast.png", 3)
        return score

# 점수 증가 아이템
class ScoreItem:
    def __init__(self, width, speed):
        x = random.randint(0, width - 15)
        self.position = np.array([x, -15, x + 15, 0])
        self.speed = speed
        self.image = Image.open("scoreItem.png").convert("RGBA").resize((30, 30))

    def move(self):
        self.position[1] += self.speed
        self.position[3] += self.speed

    def is_out_of_bounds(self, height):
        return self.position[1] > height

    def apply_effect(self, player, score):
        return score + 25
