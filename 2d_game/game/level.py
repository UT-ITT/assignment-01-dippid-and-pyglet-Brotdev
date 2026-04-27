from pyglet import graphics, gl, shapes, text
from pyglet.math import Vec2
import random
import math

from game.enemy import Enemy

def draw_grid(win, player_pos: Vec2) -> None:
    batch = graphics.Batch()

    spacing = 80

    # Calculate view area
    start_x = int(math.floor((player_pos.x - win.width / 2) / spacing)) * spacing
    end_x = int(math.ceil(player_pos.x + win.width / 2))
    start_y = int(math.floor((player_pos.y - win.height / 2) / spacing)) * spacing
    end_y = int(math.ceil(player_pos.y + win.height / 2))

    lines = []

    # Draw vertical lines
    for y in range(start_y, end_y, 80):
        lines.append(shapes.Line(start_x, y, end_x, y, 1, color=(128, 128, 128), batch=batch))

    # Draw horizontal lines
    for x in range(start_x, end_x, 80):
        lines.append(shapes.Line(x, start_y, x, end_y, 1, color=(128, 128, 128), batch=batch))

    batch.draw()

class Level:
    def __init__(self, player):
        self.spawn_timer = 0.0
        self.player = player
        self.points = []
        self.enemies = []

        self.shape = shapes.Circle(0.0, 0.0, 2000.0, None, (240, 240, 240))
        self.scoreboard = text.Label('',
                                     font_name='Times New Roman',
                                     font_size=24,
                                     x=0,
                                     y=0,
                                     color=(0,0,0),
                                     multiline=True,
                                     width=320,
                                     anchor_x='right',
                                     anchor_y='top')


        self.popup_label = text.Label('Press Button 1 to start\n\nUse Button 1 to sprint during gameplay',
                                    font_name='Times New Roman',
                                    font_size=32,
                                    x=0,
                                    y=0,
                                    color=(0,0,0),
                                    multiline=True,
                                    width=450,
                                    anchor_x='center',
                                    anchor_y='top')

    # Restart/Start game
    # Reset enemies and points
    # And make player visible
    def restart(self) -> None:
        self.player.reset()
        self.points = []
        self.enemies = []

        # Spawn a few points/enemies
        for i in range(20):
            self.spawn_enemy()
            self.spawn_point()

    # Helper function to spawn enemies
    def spawn_enemy(self) -> None:

        # Get a random position inside the game-area
        pos = Vec2(random.random() * 2.0 - 1.0, random.random() * 2.0 - 1.0).normalize() * (random.random() * 2000.0)

        # If the distance to the player is to small
        # find another position
        while pos.distance(self.player.pos) < 100.0:
            pos = Vec2(random.random() * 2.0 - 1.0, random.random() * 2.0 - 1.0).normalize() * (random.random() * 2000.0)
        self.enemies.append(Enemy(pos))

    def spawn_point(self) -> None:

        # Get a random position inside the game-area
        pos = Vec2(random.random() * 2.0 - 1.0, random.random() * 2.0 - 1.0).normalize() * (random.random() * 2000.0)
        self.points.append((shapes.Circle(pos.x, pos.y, 10, None, (0, max(80, int(255 * random.random())), 0)), pos))

    def update(self, delta: float) -> None:
        # If game is finished abort
        if len(self.enemies) < 1: return

        # Only spawn points every 0.1 seconds
        self.spawn_timer += delta
        if (self.spawn_timer > 0.1):
            self.spawn_timer -= 0.1
            if (len(self.points) < 2000 and random.random() > 0.5):
                self.spawn_point()

        # Make points collectable by player/enemy
        for point in self.points.copy():
            if self.player.contains(point[1], 10.0):
                self.points.remove(point)
                self.player.add_points(100)
            else:
                for enemy in self.enemies:
                    if enemy.contains(point[1], 10.0):
                        self.points.remove(point)
                        enemy.add_points(100)
                        break

        # Make enemies collectable by player/enemy
        for enemy in self.enemies.copy():
            # If player bigger then eat enemy
            if self.player.contains(enemy.pos, math.sqrt(enemy.mass)) and enemy.mass < self.player.mass - 100.0:
                self.enemies.remove(enemy)
                self.player.add_points(enemy.mass)
                continue
            # If enemy bigger then eat player
            elif self.player.alive and enemy.contains(self.player.pos, math.sqrt(self.player.mass)) and self.player.mass < enemy.mass - 100.0:
                enemy.add_points(self.player.mass)
                self.player.alive = False

            enemy.update(delta, self.player)

            # Check if enemies can eat each other
            for enemyB in self.enemies.copy():
                if enemyB.contains(enemy.pos, math.sqrt(enemy.mass)) and enemy.mass < enemyB.mass - 100.0:
                    self.enemies.remove(enemy)
                    enemyB.add_points(enemy.mass)
                    break

    def draw(self, win) -> None:

        # Draw white game area
        self.shape.draw()

        # Draw grid on top of game area
        draw_grid(win, self.player.pos)


        # If player is not alive then
        # either gameover or
        # game has not yet started
        if not self.player.alive:
            if len(self.enemies) > 0:
                self.popup_label.text = 'You Lost\nPress Button 1 to restart'
            self.popup_label.x = self.player.pos.x
            self.popup_label.y = self.player.pos.y + win.height // 2 - 80
            self.popup_label.draw()
            return

        # Draw points
        for point in self.points:
            point[0].draw()

        # If there are no enemies
        # then player has won
        # and we need to handle
        # the player differently
        if len(self.enemies) < 1:
            self.player.hidden = True
            self.player.shape.draw()
            self.popup_label.text = 'You Won\nPress Button 1 to restart'
            self.popup_label.x = self.player.pos.x
            self.popup_label.y = self.player.pos.y + win.height // 2 - 80
            self.popup_label.draw()
            return

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw()

        # Draw scoreboard
        self.scoreboard.x = self.player.pos.x + win.width // 2 - 20
        self.scoreboard.y = self.player.pos.y + win.height // 2 - 20
        self.scoreboard.text = f'Your Score: {self.player.mass}\nTop Score: {max(max(self.enemies, key=lambda x: x.mass).mass, self.player.mass)}\nEnemies:\t{len(self.enemies)}'
        self.scoreboard.draw()
