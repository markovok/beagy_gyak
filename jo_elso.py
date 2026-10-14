from sense_hat import SenseHat
from random import randint
from time import sleep

sense = SenseHat()

x = 3  # A madár a kijelző közepéről indul
y = 2  # Fix oszlop pozíció
game_over = False

# Színek
r = (255, 0, 0)  # Piros (cső)
o = (0, 0, 0)  # Fekete (háttér)
w = (255, 255, 255)  # Fehér (madár)

game_space = [o] * 64


# Ütközésvizsgálat a madár és a csövek/plafon/padló között
def check_collision():
    global game_over
    # Ha a madár csőnek csapódik
    if game_space[x * 8 + y] == r:
        game_over = True


# Ugrás kezelése: A joystick UP gombjára a madár emelkedik
def flap_bird(event):
    global x
    if event.action == "pressed" and event.direction == "up":
        sense.set_pixel(y, x, o)  # Előző pozíció törlése
        if x > 0:
            x -= 1  # Ugrás felfelé 1 egységgel
        sense.set_pixel(y, x, w)  # Új pozíció kirajzolása


# Cső generálása a jobb oldalon
def pipe_generator(space):
    for row in range(7, 64, 8):
        space[row] = r

    gap = randint(0, 5)
    for i in range(3):
        space[(gap + i) * 8 + 7] = o
    return space


# Csövek mozgatása jobbról balra
def move_pipes(space):
    for col in range(7):
        for row in range(8):
            space[row * 8 + col] = space[row * 8 + col + 1]

    for row in range(7, 64, 8):
        space[row] = o
    return space


# Csak a felfelé gombra iratkozunk fel
sense.stick.direction_up = flap_bird

# Fő játékciklus
while not game_over:
    game_space = pipe_generator(game_space)

    for i in range(3):
        sense.set_pixels(game_space)

        # --- GRAVITÁCIÓ ÉS ZUHANS ---
        sense.set_pixel(y, x, o)  # Töröljük a madár előző helyét

        if x < 7:
            x += 1  # A madár folyamatosan esik lefelé
        else:
            game_over = True  # Ha eléri a képernyő alját, veszített

        sense.set_pixel(y, x, w)  # Kirajzoljuk az új helyén

        check_collision()

        if game_over:
            break

        game_space = move_pipes(game_space)
        sleep(0.4)

# Játék vége
sense.show_message('You lose', scroll_speed=0.06)