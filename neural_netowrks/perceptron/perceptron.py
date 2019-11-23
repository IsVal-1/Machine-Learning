#!/usr/bin/python3
from graphics import *
import random

height = 2000
width = 2000
x_window = 0
y_window = 0
x_upper = 200
x_lower = -200
y_upper = 200
y_lower = -200
win = GraphWin(width = width, height = height, autoflush=False)
pts = []
slope = -2
y_int = 100
def sign(value):
    if value >= 0:
        return 1
    else:
        return -1

class Coordinate(object):
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        if self.x is None:
            self.x = random.uniform(-1, 1)
        if self.y is None: 
            self.y = random.uniform(-1, 1)
        self.bias = 1
        self.circle1 = Circle(Point(self.pixel_x(), self.pixel_y()), 2)
        self.circle2 = Circle(Point(self.pixel_x(), self.pixel_y()), 3)
    def draw(self):
        self.circle1.undraw()
        self.circle2.undraw()
        self.circle1 = Circle(Point(self.pixel_x(), self.pixel_y()), 2)
        self.circle2 = Circle(Point(self.pixel_x(), self.pixel_y()), 3)
        if self.pixel_y() > func(self.pixel_x()):
            self.label = 1
            self.circle2.setFill("white")
        else:
            self.label = -1
            self.circle2.setFill("black")
        win.flush()
        self.circle2.draw(win)
        self.circle1.draw(win)
    def __repr__(self):
        return "(%d, %d)"%(self.x, self.y)
    def __str__(self):
        return "(%d, %d)"%(self.x, self.y)
    def pixel_x(self):
        return map_to(self.x, -1, 1, -200, 200)
    def pixel_y(self):
        return map_to(self.y, -1, 1, -200, 200)

class Perceptron(object):
    num_weights = 3
    lr = 0.001
    def __init__(self):
        self.weights = []
        for i in range(self.num_weights):
            self.weights.append(random.uniform(-1, 1))
        print('init weights='+str(self.weights))
    def guess(self, inputs):
        sum = 0
        for i in range(self.num_weights):
          sum += float(inputs[i])*self.weights[i]
        output = sign(sum)
        return output
    def __repr__(self):
        return "Perceptron()"
    def __str__(self):
        return self.weights
    def train(self,inputs, target):
        error = target - self.guess(inputs)
        for i in range(self.num_weights):
            self.weights[i] += error * inputs[i]*self.lr
    def guessY(self, x):
        return -(self.weights[2]/self.weights[1]) - (self.weights[0]/self.weights[1])*x
def setup():
    create_window()
    win.getMouse()
    for i in range(500):
        coord = Coordinate()
        coord.draw()
        pts.append(coord)

def map_to(value, old_min, old_max, new_min, new_max):
    old_range = (old_max - old_min)
    if old_range == 0:
        new_value = new_min
    else:
        new_range = (new_max - new_min)
        new_value = (((value - old_min) * new_range) / old_range) + new_min
    return new_value

def create_window():
    win.setCoords(x_lower, y_lower, x_upper, y_upper) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
    win.setBackground("white")
    win.master.geometry('%dx%d+%d+%d'%(width, height, 900, 100))
    y_axis = Line(Point(0, y_upper), Point(0, y_lower))
    x_axis = Line(Point(x_lower,0), Point(x_upper,0))
    y_axis.setWidth(5)
    x_axis.setWidth(5)
    y_axis.draw(win)
    x_axis.draw(win)

def func(x):
   return slope*x+y_int 

def get_function_line():#slope, yint):
    #y=mx+b
    x1 = x_lower
    x2 = x_upper
    y1 = func(x1)#slope*(x1)+yint
    y2 = func(x2)#slope*x2+yint
    line = Line(Point(x1, y1), Point(x2, y2))
    line.setWidth(5)
    line.setFill('blue')
    return line

perc = Perceptron()
setup()
win.getMouse() # pause before closing
true_line = get_function_line()
guessed_line = get_function_line()
true_line.draw(win)
win.getMouse()
for p in pts:
    inputs = [p.x, p.y, p.bias]
    target = p.label
    guess = perc.guess(inputs)
    if guess == target:
        p.circle1.setFill("green")
    else:
        p.circle1.setFill("red")
    p.draw()
while True:
    #win.getMouse()
    pause = False
    guess_min = Coordinate(-1, perc.guessY(-1))
    guess_max = Coordinate(1, perc.guessY(1))
    guessed_line.undraw()
    guessed_line = Line(Point(guess_min.pixel_x(), guess_min.pixel_y()),
                        Point(guess_max.pixel_x(), guess_max.pixel_y()))
    guessed_line.setWidth(5)
    guessed_line.setFill('red')
    guessed_line.draw(win)
    for p in pts:
        inputs = [p.x, p.y, p.bias]
        target = p.label
        guess = perc.guess(inputs)
        perc.train(inputs, target)
        if guess == target:
            p.circle1.setFill("green")
        else:
            p.circle1.setFill("red")
            pause = True 
        p.draw()
        key = win.checkKey()
        if key == "Right":
            slope += 0.1
            if slope > 50:
                slope *= -1
        if key == "Left":
            slope -= 0.1
            if slope < -50:
                slope *= -1
        if key == "Up":
            y_int += 1
        if key == "Down":
            y_int -= 1
        if key != "":
            true_line.undraw()
            true_line = get_function_line()
            true_line.draw(win)
    #if not pause :
     #   break;
print(perc.weights)
guess_min = Coordinate(-1, perc.guessY(-1))
guess_max = Coordinate(1, perc.guessY(1))
guessed_line.undraw()
guessed_line = Line(Point(guess_min.pixel_x(), guess_min.pixel_y()),
                    Point(guess_max.pixel_x(), guess_max.pixel_y()))
guessed_line.setWidth(5)
guessed_line.setFill('red')
guessed_line.draw(win)
win.getMouse()
