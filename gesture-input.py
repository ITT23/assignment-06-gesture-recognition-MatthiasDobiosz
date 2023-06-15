# gesture input program for first task

# This is the file for the pyglet drawing and recognizing
# The actual 1$ recognizer is implemented in the recognizer.py file and a lot of helper functions are in the helpers.py-file

import pyglet
from pyglet import shapes, image
from helpers import resample, IndicativeAngle, RotateBy, ScaleTo, TranslateTo
from config import WINDOW_WIDTH, WINDOW_HEIGHT, NUMPOINTS, SQUARESIZE, ORIGIN
from recognizer import Recgonizer
from templates import Templates

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
background = image.load("images/background.jpg")


# Function to create template and save
def create_template(name, points):
    points = resample(points, NUMPOINTS)
    radians = IndicativeAngle(points)
    points = RotateBy(points, -radians)
    points = ScaleTo(points, SQUARESIZE)
    points = TranslateTo(points, ORIGIN)

    with open('templates.py', 'a') as f:
        template = {"name": name, "points": points}
        f.write("\n")
        f.write(str(template))
        f.close()


# GestureRecognizer Class to allow drawing of unistrokes
class GestureRecognizer:

    def __init__(self):
        self.isDrawing = False
        self.points = []
        self.previousPoint = None
        self.shape = shapes.Circle(x=0, y=0, radius=1, segments=20,
                                   color=(255, 255, 255))
        self.shapes = []
        self.time = None
        self.recognizer = Recgonizer(Templates, False)
        self.feedback = "Start Drawing"

    def add(self, x, y):
        if self.isDrawing and y > 200:
            if not ((x, y) in self.points):
                self.points.append((x, y))
            self.previousPoint = (x, y)

    def drawBackgroundAndLabels(self):
        background.blit(0, 0)
        pyglet.text.Label(self.feedback,
                          font_name='Times New Roman',
                          font_size=30,
                          x=250,
                          y=100,
                          color=(0, 0, 0, 255),
                          anchor_x='center',
                          anchor_y='center').draw()
        if self.time is not None:
            pyglet.text.Label(self.time + " ms",
                              font_name='Times New Roman',
                              font_size=20,
                              x=250,
                              y=50,
                              color=(0, 0, 0, 255),
                              anchor_x='center',
                              anchor_y='center').draw()

    def draw(self):
        self.drawBackgroundAndLabels()
        batch = pyglet.graphics.Batch()
        for point in self.points:
            shape = shapes.Circle(x=point[0], y=point[1], radius=1,
                                  color=(255, 0, 0), batch=batch)
            self.shapes.append(shape)
        batch.draw()
        self.shapes = []

    def eval(self):
        if len(self.points) > 0 and self.isDrawing:
            self.feedback = "detecting"
            self.feedback, self.time = self.recognizer.recognize(self.points)
            self.points = []

    # Function that was used to create the unistroke-templates
    def create(self):
        create_template("NAME", self.points)


gestureRecognizer = GestureRecognizer()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        gestureRecognizer.isDrawing = True

    pass


@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        gestureRecognizer.eval()
        # gestureRecognizer.create()
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
        pyglet.exit()


pyglet.app.run()
