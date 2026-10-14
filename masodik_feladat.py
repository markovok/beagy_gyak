from sense_hat import SenseHat
from random import randint
import time

sense = SenseHat()

# Színek
w = (255, 255, 255)  # Fehér (kosár)
r = (255, 0, 0)      # Piros (gyümölcs)
o = (0, 0, 0)        # Fekete (háttér)

# Kezdőpozíció a kosárnak (3, 3)
basket_x = 3
basket_y = 3

score = 0

# Gyümölcs véletlenszerű generálása
def generate_fruit():
    fx = randint(0, 7)
    fy = randint(0, 7)
    return fx, fy

# Első gyümölcs legyártása
fruit_x, fruit_y = generate_fruit()

# Biztosítjuk, hogy a gyümölcs ne a kosár tetejére teremjen rögtön az elején
while fruit_x == basket_x and fruit_y == basket_y:
    fruit_x, fruit_y = generate_fruit()

# Joystick mozgáskezelő
def move_basket(event):
    global basket_x, basket_y
    if event.action == "pressed":
        if event.direction == "up" and basket_y > 0:
            basket_y -= 1
        elif event.direction == "down" and basket_y < 7:
            basket_y += 1
        elif event.direction == "left" and basket_x > 0:
            basket_x -= 1
        elif event.direction == "right" and basket_x < 7:
            basket_x += 1

sense.stick.direction_any = move_basket

# Időmérés indítása
start_time = time.time()
duration = 30  # 30 másodperc

sense.clear()

# Játékciklus (pontosan 30 másodpercig fut)
while time.time() - start_time < duration:
    # 1. Töröljük a kijelzőt (háttér fekete)
    sense.clear()

    # 2. Ütközésvizsgálat (Gyümölcs elkapása)
    if basket_x == fruit_x and basket_y == fruit_y:
        score += 1
        fruit_x, fruit_y = generate_fruit()

    # 3. Kirajzoljuk a gyümölcsöt és a kosarat
    sense.set_pixel(fruit_x, fruit_y, r)
    sense.set_pixel(basket_x, basket_y, w)

    # Egy egészen pici szünet a CPU kímélése miatt (nem akasztja meg az irányítást)
    time.sleep(0.02)

# 30 másodperc leteltével a játék vége
sense.clear()
sense.show_message("Score: {}".format(score), scroll_speed=0.06, text_colour=w)