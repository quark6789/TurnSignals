import board
import digitalio
import neopixel
import time


AMBER = (255, 110, 0)
OFF = (0, 0, 0)
BLINK_DURATION = .4


class ButtonStatus():
    def __init__(self):
        self.pushed = False
        self.pushed_prev = False

    def update(self, currently_pushed: bool):
        self.pushed_prev = self.pushed
        self.pushed = currently_pushed

    def was_pushed(self):
        return self.pushed and not self.pushed_prev


class BlinkerStatus():
    def __init__(self):
        self.blink_duration = BLINK_DURATION

        self.enabled = False
        self.now = 0
        self.last_reset_time = 0

    def update(self, now: float):
        self.now = now

    def enable(self):
        self.enabled = True
        self.last_reset_time = self.now

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled

    def on(self):
        if not self.enabled:
            return False

        time_since_last_reset = self.now - self.last_reset_time
        if time_since_last_reset < self.blink_duration:
            return True
        else:
            if time_since_last_reset > 2 * self.blink_duration:
                self.last_reset_time = now
            return False


# Hardware setup
leds = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.02, auto_write=False)
left_button = digitalio.DigitalInOut(board.BUTTON_A)
right_button= digitalio.DigitalInOut(board.BUTTON_B)
left_button.switch_to_input(pull=digitalio.Pull.DOWN)
right_button.switch_to_input(pull=digitalio.Pull.DOWN)

left_blinker = BlinkerStatus()
right_blinker = BlinkerStatus()
left_button_status = ButtonStatus()
right_button_status = ButtonStatus()

while True:
    now = time.monotonic()
    left_blinker.update(now)
    right_blinker.update(now)
    left_button_status.update(left_button.value)
    right_button_status.update(right_button.value)

    if left_button_status.was_pushed() and right_button_status.was_pushed():
        left_blinker.disable()
        right_blinker.disable()
    elif left_button_status.was_pushed():
        if left_blinker.is_enabled():
            left_blinker.disable()
        else:
            left_blinker.enable()
            right_blinker.disable()
    elif right_button_status.was_pushed():
        if right_blinker.is_enabled():
            right_blinker.disable()
        else:
            right_blinker.enable()
            left_blinker.disable()

    if left_blinker.on():
        leds[0:5] = [AMBER] * 5
    else:
        leds[0:5] = [OFF] * 5
    if right_blinker.on():
        leds[5:10] = [AMBER] * 5
    else:
        leds[5:10] = [OFF] * 5
    leds.show()
