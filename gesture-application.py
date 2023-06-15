import random
import pyglet
from pyglet import shapes, clock, image
from helpers import resample, IndicativeAngle, RotateBy, ScaleTo, TranslateTo
from config import WINDOW_WIDTH, WINDOW_HEIGHT, NUMPOINTS, SQUARESIZE, ORIGIN
from recognizer import Recgonizer
from game_unistrokes import GAME_TEMPLATES
import time

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
background = image.load("images/background.jpg")


# Function used to create templates for the game
def create_template(name, points):
    points = resample(points, NUMPOINTS)
    radians = IndicativeAngle(points)
    points = RotateBy(points, -radians)
    points = ScaleTo(points, SQUARESIZE)
    points = TranslateTo(points, ORIGIN)

    with open('game_unistrokes.py', 'a') as f:
        template = {"name": name, "points": points}
        f.write("\n")
        f.write(str(template))
        f.close()


class Game:

    def __init__(self):
        # init variables
        self.recognizer = Recgonizer(GAME_TEMPLATES, True)
        self.templates = GAME_TEMPLATES

        # states
        self.gameOver = False
        self.gameStarted = False
        self.isDrawing = False
        self.displayTemplate = False
        self.correctTemplate = None
        self.score = 0

        # timer
        self.currentTimeFromZero = None

        # save points/shapes
        self.points = []
        self.previousPoint = None
        self.shapes = []
        self.templateShapes = []
        self.templateBatch = None

        self.feedback = "Start Drawing"

    def reset(self):
        self.gameOver = False
        self.gameStarted = False
        self.isDrawing = False
        self.displayTemplate = False
        self.correctTemplate = None
        self.score = 0
        self.points = []
        self.previousPoint = None
        self.shapes = []
        self.templateShapes = []
        self.templateBatch = None
        self.feedback = "Start Drawing"
        self.currentTimeFromZero = None

    def update(self, delta_time):
        if self.gameStarted:
            if self.displayTemplate:
                if self.currentTimeFromZero is None:
                    self.currentTimeFromZero = time.time()
                currentTime = time.time()
                timediff = currentTime - self.currentTimeFromZero
                if timediff > 3:
                    self.templateBatch = None
                    self.templateShapes = []
                    self.displayTemplate = False
                    self.currentTimeFromZero = None
                else:
                    if timediff < 1:
                        self.feedback = "3"
                    elif timediff < 2:
                        self.feedback = "2"
                    elif timediff < 2.9:
                        self.feedback = "1"

            elif not self.isDrawing:
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

    def drawStartScreen(self):
        pyglet.text.Label("Draw after me",
                          font_name='Times New Roman',
                          font_size=30,
                          x=250,
                          y=500,
                          color=(255, 255, 255, 255),
                          anchor_x='center',
                          anchor_y='center').draw()
        pyglet.text.Label(
            "A symbol will appear on the screen for some time,",
            font_name='Times New Roman',
            font_size=15,
            x=250,
            y=400,
            color=(255, 255, 255, 255),
            anchor_x='center',
            anchor_y='center').draw()
        pyglet.text.Label(
            "if you can correctly re-draw it the game will continue",
            font_name='Times New Roman',
            font_size=15,
            x=250,
            y=350,
            color=(255, 255, 255, 255),
            anchor_x='center',
            anchor_y='center').draw()
        pyglet.text.Label("Press Space to Start!",
                          font_name='Times New Roman',
                          font_size=15,
                          x=250,
                          y=200,
                          color=(255, 255, 255, 255),
                          anchor_x='center',
                          anchor_y='center').draw()

    def drawEndScreen(self):
        pyglet.text.Label("Game over!",
                          font_name='Times New Roman',
                          font_size=30,
                          x=250,
                          y=500,
                          color=(255, 255, 255, 255),
                          anchor_x='center',
                          anchor_y='center').draw()
        pyglet.text.Label(
            "Score: " + str(self.score),
            font_name='Times New Roman',
            font_size=15,
            x=250,
            y=350,
            color=(255, 255, 255, 255),
            anchor_x='center',
            anchor_y='center').draw()

        pyglet.text.Label("Press 2 to Re-Start!",
                          font_name='Times New Roman',
                          font_size=15,
                          x=250,
                          y=300,
                          color=(255, 255, 255, 255),
                          anchor_x='center',
                          anchor_y='center').draw()
        pyglet.text.Label("Press 3 to End the Game!",
                          font_name='Times New Roman',
                          font_size=15,
                          x=250,
                          y=250,
                          color=(255, 255, 255, 255),
                          anchor_x='center',
                          anchor_y='center').draw()

    def draw(self):
        if self.gameOver:
            self.drawEndScreen()
        elif not self.gameStarted:
            self.drawStartScreen()
        elif self.displayTemplate:
            self.game_draw()
        elif self.isDrawing:
            self.player_draw()
        else:
            self.drawBackgroundAndLabels()

    def init_template(self):
        if len(self.templateShapes) == 0:
            template = random.choice(self.templates)
            self.correctTemplate = template["name"]
            batch = pyglet.graphics.Batch()
            for point in template["points"]:
                shape = shapes.Circle(x=point[0], y=point[1], radius=1,
                                      color=(0, 0, 255), batch=batch)
                self.templateShapes.append(shape)
            self.templateBatch = batch

    def game_draw(self):
        if not self.templateBatch:
            self.init_template()
        else:
            self.drawBackgroundAndLabels()
            self.templateBatch.draw()

    def player_draw(self):
        self.drawBackgroundAndLabels()
        batch = pyglet.graphics.Batch()
        for point in self.points:
            shape = shapes.Circle(x=point[0], y=point[1], radius=1,
                                  color=(0, 255, 0), batch=batch)
            self.shapes.append(shape)
        batch.draw()
        self.shapes = []

    def eval(self):
        if len(self.points) > 0 and self.isDrawing:
            prediction, _ = self.recognizer.recognize(self.points)
            if prediction == self.correctTemplate:
                self.feedback = "Nice!"
                self.score += 1
            else:
                self.gameOver = True
            self.points = []
            self.isDrawing = False
            self.displayTemplate = True

    def create(self):
        create_template("The letter S", self.points)


game = Game()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if game.gameStarted and not game.displayTemplate:
            game.feedback = "you are doing great"
            game.isDrawing = True

    pass


@window.event
def on_mouse_release(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if game.gameStarted and not game.displayTemplate:
            game.eval()
    pass


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if game.gameStarted and not game.displayTemplate:
        if game.isDrawing:
            game.add(x, y)
    pass


@window.event
def on_draw():
    window.clear()
    game.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key._3:
        pyglet.app.exit()
    elif symbol == pyglet.window.key.SPACE:
        game.gameStarted = True
        game.displayTemplate = True
    elif symbol == pyglet.window.key._2:
        game.reset()


clock.schedule_interval(game.update, 0.001)

pyglet.app.run()
# application for task 3
