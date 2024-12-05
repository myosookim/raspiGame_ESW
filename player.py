from PIL import Image
import time
import numpy as np


class Player:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = np.array([width // 2 - 15, height - 45, width // 2 + 15, height - 15])
        self.base_image = Image.open("player.png").convert("RGBA").resize((30, 30))
        self.player_image = self.base_image
        self.speed = 10
        self.base_speed = 10
        self.hp = 3
        self.max_hp = 3

        self.current_state = "default"
        self.image_change_start_time = None

        self.jump_height = 75
        self.jump_duration = 0.5
        self.is_jumping = False
        self.jump_start_time = None

    def move(self, command):
        current_speed = self.speed
        if command['left_pressed'] and self.position[0] > 0:
            self.position[0] -= current_speed
            self.position[2] -= current_speed
        if command['right_pressed'] and self.position[2] < self.width:
            self.position[0] += current_speed
            self.position[2] += current_speed

    def jump(self):
        if self.is_jumping:
            elapsed = time.time() - self.jump_start_time
            if elapsed < self.jump_duration:
                jump_progress = elapsed / self.jump_duration
                offset = self.jump_height * (1 - 4 * (jump_progress - 0.5) ** 2)
                self.position[1] = self.height - 45 - offset
                self.position[3] = self.height - 15 - offset
            else:
                self.is_jumping = False
                self.position[1] = self.height - 45
                self.position[3] = self.height - 15

    def reset_to_base(self):
        self.current_state = "default"
        self.player_image = self.base_image
        self.speed = self.base_speed

    def update_state(self):
        if self.current_state != "default":
            elapsed_time = time.time() - self.image_change_start_time
            if self.current_state == "hit" and elapsed_time >= 0.5:
                self.reset_to_base()
            elif self.current_state == "shielded" and elapsed_time >= 3:
                self.reset_to_base()
            elif self.current_state == "healed" and elapsed_time >= 1:
                self.reset_to_base()
            elif self.current_state == "scored" and elapsed_time >= 1:
                self.reset_to_base()
            elif self.current_state == "fast" and elapsed_time >= 3:
                self.reset_to_base()

    def change_state(self, new_state, new_image, duration):
        self.current_state = new_state
        self.player_image = Image.open(new_image).convert("RGBA").resize((30, 30))
        self.image_change_start_time = time.time()
        if new_state == "fast":
            self.speed = self.base_speed * 2
