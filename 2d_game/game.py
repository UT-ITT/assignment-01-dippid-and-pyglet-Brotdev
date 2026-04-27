import pyglet
from pyglet import window, shapes
from pyglet.gl import glClearColor
from pyglet.math import Mat4, Vec3, Vec2

from DIPPID import SensorUDP

from game.level import Level
from game.player import Player

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
glClearColor(0.6, 0.6, 0.6, 0.9)

PORT = 5700
sensor = SensorUDP(PORT)

player = Player()
level = Level(player)

@win.event
def on_draw():
    win.clear()
    win.view = Mat4.from_translation(Vec3(win.width // 2 - player.pos.x, win.height // 2 - player.pos.y, 0))

    level.draw(win)
    player.draw()

wish_dir = Vec2(0.0, 0.0)

# Code for debugging with keyboard
#@win.event
#def on_key_press(symbol, modifiers):
#    global level
#    global wish_dir
#    if symbol == window.key.W: wish_dir = wish_dir + Vec2(0.0, 1.0)
#    if symbol == window.key.S: wish_dir = wish_dir - Vec2(0.0, 1.0)
#    if symbol == window.key.A: wish_dir = wish_dir - Vec2(1.0, 0.0)
#    if symbol == window.key.D: wish_dir = wish_dir + Vec2(1.0, 0.0)
#
#    if symbol == window.key.B:
#        if player.alive and len(level.enemies) > 0:
#            player.sprint = True
#        else:
#            level.restart()

#@win.event
#def on_key_release(symbol, modifiers):
#    global wish_dir
#    if symbol == window.key.W: wish_dir = wish_dir - Vec2(0.0, 1.0)
#    if symbol == window.key.S: wish_dir = wish_dir + Vec2(0.0, 1.0)
#    if symbol == window.key.A: wish_dir = wish_dir + Vec2(1.0, 0.0)
#    if symbol == window.key.D: wish_dir = wish_dir - Vec2(1.0, 0.0)
#    if symbol == window.key.B: player.sprint = False

def update(delta: float) -> None:
    player.update(delta, wish_dir)
    level.update(delta)

def handle_dir(data) -> None:
    global wish_dir
    
    deadzone = 0.075
    if data['x'] < deadzone and data['y'] < deadzone:
        wish_dir = Vec2(0.0, 0.0)

    wish_dir = Vec2(
       max(-1.0, min(data['x'] * -2.0, 1.0)),
       max(-1.0, min(data['y'] * -2.0, 1.0))
    )

def handle_button_1(data: 0 | 1) -> None:
    if data == 1:
        if player.alive and len(level.enemies) > 0:
            player.sprint = True
        else:
            level.restart()
    elif data == 0:
        player.sprint = False

sensor.register_callback('accelerometer', handle_dir)
sensor.register_callback('button_1', handle_button_1)

pyglet.clock.schedule_interval(update, 1.0/60.0)

pyglet.app.run()
