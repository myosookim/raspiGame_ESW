from PIL import Image
import random
import numpy as np


class Obstacle:
    def __init__(self, width, speed):
        x = random.randint(0, width - 40)
        self.position = np.array([x, -40, x + 40, 0])
        self.speed = speed
        self.image = self.load_random_image()

    def load_random_image(self):
        image_choice = random.choice(["obstacle1_raspi.png", "obstacle2_raspi.png", "obstacle3_raspi.png"])
        return Image.open(image_choice).convert("RGBA").resize((40, 40))

    def move(self):
        self.position[1] += self.speed
        self.position[3] += self.speed

    def is_out_of_bounds(self, height):
        return self.position[1] > height