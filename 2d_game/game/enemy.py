import pyglet
from pyglet.math import Vec2
from pyglet import window, shapes
import random
import math
 
# Helper function to move vector towards
# another vector (smoothing)
def move_toward(current: Vec2, target: Vec2, delta: float) -> Vec2:
    diff = target - current
    dist = diff.length()

    if dist <= delta or dist == 0:
        return target

    return current + diff.normalize() * delta

class Enemy:
    def __init__(self, pos: Vec2):
        self.max_speed = 75.0
        self.mass = 200.0 + int(random.random() * 500.0)
        self.pos = pos
        self.vel = Vec2(0.0, 0.0)
        self.accl = 200.0

        self.target_pos = Vec2(100.0, 100.0)

        self.shape = shapes.Circle(self.pos[0], self.pos[1], math.sqrt(self.mass), None, (0, int(255 * random.random()), int(255 * random.random())))

    # Check if enemy contains other object
    def contains(self, pos: Vec2, radius: float):
        return pos.distance(self.pos) < math.sqrt(self.mass) - radius

    def add_points(self, amount: float):
        self.mass += amount
        self.shape.radius = math.sqrt(self.mass)

    def update(self, delta: float, player) -> None:

        # Player is visible to enemy
        # then chase player
        if self.pos.distance(player.pos) < 400.0 and player.mass < self.mass - 150.0:
            self.target_pos = player.pos
        elif self.pos.distance(self.target_pos) < 10.0:
            self.target_pos = Vec2(random.random(), random.random()).normalize() * (random.random() * 2000.0)
        
        # Try to move to target position
        self.vel = move_toward(self.vel, (self.target_pos - self.pos).normalize() * self.max_speed, self.accl * delta)
        self.pos = self.pos + self.vel * delta

        self.shape.x = self.pos.x
        self.shape.y = self.pos.y

    def draw(self) -> None:
        self.shape.draw()
