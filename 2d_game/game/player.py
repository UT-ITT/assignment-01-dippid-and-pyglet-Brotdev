import pyglet
from pyglet import window, shapes, text
from pyglet.math import Vec2
import math

# Helper function to move vector towards
# another vector (smoothing)
def move_toward(current: Vec2, target: Vec2, delta: float) -> Vec2:
    diff = target - current
    dist = diff.length()

    if dist <= delta or dist == 0:
        return target

    return current + diff.normalize() * delta

class Player:
    def __init__(self):
        self.reset()
        self.alive = False

    # Reset player upon
    # gamestart/restart
    def reset(self) -> None:
        self.timer = 0.0
        self.sprint = False
        self.max_speed = 80.0
        self.mass = 200.0
        self.pos = Vec2(0.0, 0.0)
        self.vel = Vec2(0.0, 0.0)
        self.accl = 200.0
        self.alive = True
        self.shape = shapes.Circle(self.pos[0], self.pos[1], math.sqrt(self.mass), None, (255, 0, 0))
        self.hidden = False

    # Check if player contains other object
    def contains(self, pos: Vec2, radius: float) -> bool:
        return self.alive and pos.distance(self.pos) < math.sqrt(self.mass) - radius

    # Add points to player
    def add_points(self, amount: float) -> None:
        self.mass += amount
        self.shape.radius = math.sqrt(self.mass)

    def update(self, delta: float, wish_dir: Vec2) -> None:
        if not self.alive: return

        if self.sprint:
            self.timer += delta

        # Subtract point every
        # 0.25 seconds while sprinting
        if self.timer > 0.25:
            self.timer -= 0.25
            self.mass -= 1

        # Update position
        self.vel = move_toward(self.vel, wish_dir * (self.max_speed + int(self.sprint) * 80), self.accl * delta)
        self.pos = self.pos + self.vel * delta
        self.pos = self.pos.normalize() * min(self.pos.length(), 2000.0)

        self.shape.x = self.pos.x
        self.shape.y = self.pos.y

    def draw(self) -> None:
        if not self.alive or self.hidden: return
        self.shape.draw()
