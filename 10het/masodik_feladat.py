import RPi.GPIO as io
import time
import math

TRIG = 17
ECHO = 27

LED_R = 20
LED_G = 16
LED_B = 21

BUZZER = 24
LDR_PIN = 23

C = 0.00001
RMAX = 10000
TMAX = RMAX * C
VS = 1.95

DARK_THRESHOLD_KOHM = 15.0

io.setmode(io.BCM)
io.setup(TRIG, io.OUT)
io.setup(ECHO, io.IN)

io.setup(LED_R, io.OUT)
io.setup(LED_G, io.OUT)
io.setup(LED_B, io.OUT)

io.setup(BUZZER, io.OUT)
buzzer_pwm = io.PWM(BUZZER, 1000)
buzzer_pwm.start(0)


def set_led(r, g, b):
    io.output(LED_R, io.HIGH if r else io.LOW)
    io.output(LED_G, io.HIGH if g else io.LOW)
    io.output(LED_B, io.HIGH if b else io.LOW)


def measure_ldr():
    io.setup(LDR_PIN, io.OUT)
    io.output(LDR_PIN, io.HIGH)
    time.sleep(5 * TMAX)

    io.setup(LDR_PIN, io.IN)
    start_time = time.time()

    while io.input(LDR_PIN) == io.HIGH:
        if time.time() - start_time > 0.2:
            return 100.0

    dt = time.time() - start_time
    r_val = - (0.85 * dt / (C * math.log(1.0 - (VS / 3.3))))
    return r_val / 1000.0


def measure_distance():
    io.output(TRIG, io.LOW)
    time.sleep(0.02)

    io.output(TRIG, io.HIGH)
    time.sleep(0.00001)
    io.output(TRIG, io.LOW)

    timeout = time.time()
    while io.input(ECHO) == 0:
        if time.time() - timeout > 0.04:
            return 0.0

    pulse_start = time.perf_counter_ns()
    timeout = time.time()
    while io.input(ECHO) == 1:
        if time.time() - timeout > 0.04:
            return 0.0

    duration_us = (time.perf_counter_ns() - pulse_start) / 1000.0
    distance = round(duration_us / 58.0, 2)
    return distance if distance < 400.0 else 0.0


def play_tone(freq, duration):
    if freq == 0:
        buzzer_pwm.ChangeDutyCycle(0)
    else:
        buzzer_pwm.ChangeFrequency(freq)
        buzzer_pwm.ChangeDutyCycle(50)
    time.sleep(duration)
    buzzer_pwm.ChangeDutyCycle(0)


def play_greeting():
    set_led(False, True, True)
    notes = [523, 659, 784]
    for n in notes:
        play_tone(n, 0.12)
        time.sleep(0.03)


def play_frightened():
    set_led(True, False, False)
    buzzer_pwm.ChangeFrequency(2000)
    buzzer_pwm.ChangeDutyCycle(50)
    time.sleep(0.08)
    set_led(False, False, False)
    buzzer_pwm.ChangeDutyCycle(0)
    time.sleep(0.08)


try:
    was_greeting_played = False
    while True:
        ldr_kohm = measure_ldr()

        if ldr_kohm > DARK_THRESHOLD_KOHM:
            set_led(False, False, False)
            buzzer_pwm.ChangeDutyCycle(0)
            was_greeting_played = False
            time.sleep(0.3)
            continue

        d = measure_distance()

        if 20.0 <= d <= 50.0:
            if not was_greeting_played:
                play_greeting()
                was_greeting_played = True
            set_led(False, False, True)
            time.sleep(0.1)

        elif 0.0 < d < 20.0:
            was_greeting_played = False
            play_frightened()

        else:
            set_led(False, True, False)
            buzzer_pwm.ChangeDutyCycle(0)
            was_greeting_played = False
            time.sleep(0.1)

finally:
    buzzer_pwm.stop()
    set_led(False, False, False)
    io.cleanup()