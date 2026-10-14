# Import necessary modules
from sense_hat import SenseHat
import random
from time import sleep
sense = SenseHat()
# Auxiliary variables to speed control, basket positioning, etc.
score = 0
speed = 0.4
basket = [7,4]
game_alive = True
# Initialize game space:
w = (0,0,0)
r = (255,0,0)
b = (0,0,255)
game_space = [w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,w,w,w,w,w,
w,w,w,b,b,w,w,w]
# Create a function which updates game space
def update_space(x, y, colour):
# index from from coordinate
p = 8 * x + y
game_space[p] = colour
sense.set_pixels(game_space)
# Create a handler function to the joystick left and right movements.
# Some data called event will be passed to this function.
# The event contains information about what was happened with the Sense HAT joystick.
def left(event):
if event.action == "pressed":
#the basket reached the left side
if basket[1] <= 1:
pass
#move basket one position left
else:
update_space(basket[0], basket[1], w)
basket[1] -= 1
update_space(basket[0], basket[1] - 1, b)
def right(event):
if event.action == "pressed":
# the basket reached the right side
if basket[1] >= 7:
pass
# move basket one position left
else:
update_space(basket[0], basket[1] - 1, w)
basket[1] += 1
update_space(basket[0], basket[1], b)
# Joystick trigger events
sense.stick.direction_left = left
sense.stick.direction_right = right
# Initialize game
sense.clear()
sense.set_pixels(game_space)
# Game loop
while game_alive:
# initialize position and direction of the ball
# (x,y) - ball coordinate, d - direction
x = 0
y = random.randint(0,7)
# random.choice() - randomly selects a value from a list
ball_lr = random.choice([-1,1])
# put the ball into the game space
update_space(x, y, r)
# while the ball is in the game space
while True:
sleep(speed)
# clear old ball position
update_space(x, y, w)
# ball reached the edge of game space
if x == 7:
if y == basket[1] - 1 or y == basket[1]:
#ball is in the basket
update_space(x, y, b)
score += 1
break
else:
#ball is out of the space
game_alive = False
break
#ball reached the right side of the space
if y == 7 and ball_lr == 1:
ball_lr = -1
#ball reached the left side of the space
elif y == 0 and ball_lr == -1:
ball_lr = 1
y += ball_lr
x += 1
update_space(x, y, r)
# At the end of the game, print out the "Game over!" message and the score
sense.clear()
sense.show_message("Game over!", scroll_speed=0.05, back_colour=w)
sense.show_message("Score: {}".format(str(score)), scroll_speed=0.05, back_colour=w)
Pong is one of the first computer games that ever created. Today, the Pong game is considered to be t