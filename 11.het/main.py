import random
import time
import smbus
import spidev

bus = smbus.SMBus(1)
DEVICE = 0x20
IODIRA = 0x00
IODIRB = 0x01
GPIOB = 0x13
OLATA = 0x14

bus.write_byte_data(DEVICE, IODIRA, 0x00)
bus.write_byte_data(DEVICE, IODIRB, 0xFF)
bus.write_byte_data(DEVICE, OLATA, 0x00)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

MAX7219_REG_DIGIT0 = 0x1
MAX7219_REG_DIGIT1 = 0x2
MAX7219_REG_DECODEMODE = 0x9
MAX7219_REG_INTENSITY = 0xA
MAX7219_REG_SCANLIMIT = 0xB
MAX7219_REG_SHUTDOWN = 0xC

seg = {"a": 64, "b": 32, "c": 16, "d": 8, "e": 4, "f": 2, "g": 1, "dp": 128}
digits = [
    seg["a"] + seg["b"] + seg["c"] + seg["d"] + seg["e"] + seg["f"],
    seg["b"] + seg["c"],
    seg["a"] + seg["b"] + seg["d"] + seg["e"] + seg["g"],
    seg["a"] + seg["b"] + seg["c"] + seg["d"] + seg["g"],
    seg["b"] + seg["c"] + seg["f"] + seg["g"],
    seg["a"] + seg["c"] + seg["d"] + seg["f"] + seg["g"],
    seg["a"] + seg["c"] + seg["d"] + seg["e"] + seg["f"] + seg["g"],
    seg["a"] + seg["b"] + seg["c"],
    seg["a"] + seg["b"] + seg["c"] + seg["d"] + seg["e"] + seg["f"] + seg["g"],
    seg["a"] + seg["b"] + seg["c"] + seg["d"] + seg["f"] + seg["g"]
]

def initialize_seven_segment(intensity=0x8):
    spi.xfer([MAX7219_REG_DECODEMODE, 0x0])
    spi.xfer([MAX7219_REG_INTENSITY, intensity])
    spi.xfer([MAX7219_REG_SCANLIMIT, 0x1])
    spi.xfer([MAX7219_REG_SHUTDOWN, 0x1])
    spi.xfer([MAX7219_REG_DIGIT0, 0])
    spi.xfer([MAX7219_REG_DIGIT1, 0])

def display_reaction_time(seconds):
    value = int(round(seconds * 10))
    if value < 100:
        dig1 = value // 10
        dig0 = value % 10
        spi.xfer([MAX7219_REG_DIGIT0, digits[dig1] + seg["dp"]])
        spi.xfer([MAX7219_REG_DIGIT1, digits[dig0]])
    else:
        spi.xfer([MAX7219_REG_DIGIT0, seg["g"]])
        spi.xfer([MAX7219_REG_DIGIT1, seg["g"]])

initialize_seven_segment()

try:
    while True:
        while bus.read_byte_data(DEVICE, GPIOB) != 0:
            pass

        delay = random.uniform(1.0, 5.0)
        time.sleep(delay)

        bus.write_byte_data(DEVICE, OLATA, 0x01)
        start_time = time.perf_counter()

        while bus.read_byte_data(DEVICE, GPIOB) == 0:
            pass

        elapsed = time.perf_counter() - start_time
        bus.write_byte_data(DEVICE, OLATA, 0x00)

        display_reaction_time(elapsed)
        print("Reaction time: {:.1f} s".format(elapsed))
        time.sleep(2.0)
        spi.xfer([MAX7219_REG_DIGIT0, 0])
        spi.xfer([MAX7219_REG_DIGIT1, 0])

except KeyboardInterrupt:
    pass
finally:
    bus.write_byte_data(DEVICE, OLATA, 0x00)
    spi.xfer([MAX7219_REG_DIGIT0, 0])
    spi.xfer([MAX7219_REG_DIGIT1, 0])
    spi.close()