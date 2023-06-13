# gesture input program for first task
import pyglet
from pyglet import shapes, clock
import sys

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)


class GestureRecognizer:

    def __init__(self):
        self.isDrawing = False
        self.points = []
        self.shape = shapes.Circle(x=0, y=0, radius=1, segments=20,
                                   color=(255, 255, 255))
        self.shapes = []

    def add(self, x, y):
        if self.isDrawing:
            self.points.append([x, y])

    def draw(self):
        batch = pyglet.graphics.Batch()
        for point in self.points:
            shape = shapes.Circle(x=point[0], y=point[1], radius=1,
                          color=(255, 0, 0), batch=batch)
            self.shapes.append(shape)
        batch.draw()
        self.shapes = []


gestureRecognizer = GestureRecognizer()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        gestureRecognizer.isDrawing = True
    pass


@window.event
def on_mouse_release(x, y, button, modifiers):
    pass


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if gestureRecognizer.isDrawing:
        gestureRecognizer.add(x, y)
    pass


@window.event
def on_draw():
    window.clear()
    gestureRecognizer.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key._3:
        sys.exit()


pyglet.app.run()
