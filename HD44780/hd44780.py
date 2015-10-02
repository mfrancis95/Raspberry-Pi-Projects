import RPi.GPIO as GPIO
from time import sleep

class HD44780:

    def __del__(self):
        GPIO.cleanup()

    def __init__(self, pin_rs = 25, pin_e = 24, pin_bits = [23, 17, 27, 22]):
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pin_bits = pin_bits

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(pin_rs, GPIO.OUT)
        GPIO.setup(pin_e, GPIO.OUT)

        for pin in pin_bits:
            GPIO.setup(pin, GPIO.OUT)

        self.write(0x33)
        self.write(0x32)
        self.write(0x28)
        self.clear()
        self.write(0x03)
        self.write(0x0C)
        self.cursor_home()

    def character(self, character):
        if character == '\n':
            self.write(0x80 + 64)
        else:
            self.write(ord(character) if type(character) is str else character, True)

    def clear(self):
        self.write(0x01)

    def create_character(self, which, data):
        self.write(0x40 + which * 8)
        for i in data:
            self.write(i, True)

    def cursor_home(self):
        self.write(0x02)

    def message(self, text, delay = 0):
        for c in text:
            sleep(delay)
            self.character(c)

    def pulse(self):
        sleep(0.00005)
        GPIO.output(self.pin_e, True)
        sleep(0.00005)
        GPIO.output(self.pin_e, False)
        sleep(0.00005)

    def write(self, value, char_mode = False):
        GPIO.output(self.pin_rs, char_mode)

        GPIO.output(self.pin_bits[0], value & 0x10 == 0x10)
        GPIO.output(self.pin_bits[1], value & 0x20 == 0x20)
        GPIO.output(self.pin_bits[2], value & 0x40 == 0x40)
        GPIO.output(self.pin_bits[3], value & 0x80 == 0x80)

        self.pulse()

        GPIO.output(self.pin_rs, char_mode)

        GPIO.output(self.pin_bits[0], value & 0x01 == 0x01)
        GPIO.output(self.pin_bits[1], value & 0x02 == 0x02)
        GPIO.output(self.pin_bits[2], value & 0x04 == 0x04)
        GPIO.output(self.pin_bits[3], value & 0x08 == 0x08)

        self.pulse()
