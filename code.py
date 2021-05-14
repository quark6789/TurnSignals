import board
import digitalio
import neopixel
import time


AMBER = (255, 110, 0)
OFF = (0, 0, 0)
BLINK_DURATION = .4


class PixelBlinker():
    def __init__(self,
                 color1: tuple,
                 color2: tuple,
                 blink_duration: float,
    ):
        self.color1 = color1
        self.color2 = color2
        self.blink_duration = blink_duration

        self.current_color = 1
        self.last_toggle = 0

    def update(self, now: float):
        if (now - self.last_toggle) > (self.blink_duration):
            self.current_color = 2 if self.current_color == 1 else 1
            self.last_toggle = now

        if self.current_color == 1:
            return self.color1
        else:
            return self.color2


# Hardware setup
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.02, auto_write=False)
left_button = digitalio.DigitalInOut(board.BUTTON_A)
left_button.switch_to_input(pull=digitalio.Pull.DOWN)

left_pixel_blinker = PixelBlinker(AMBER, OFF, BLINK_DURATION)

while True:
    now = time.monotonic()
    pixels[0:5] = [left_pixel_blinker.update(now)] * 5
    pixels.show()
