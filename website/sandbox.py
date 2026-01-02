import time
import random
from web_graphics import WebGraphics
from web_button import WebButton
from web_display import start_web_display
from rgb_led import RGBLED

if not hasattr(time, "ticks_ms"):
    def ticks_ms():
        return int(time.monotonic() * 1000)


    time.ticks_ms = ticks_ms

if not hasattr(time, "ticks_diff"):
    def ticks_diff(end, start):
        return end - start


    time.ticks_diff = ticks_diff

start_web_display()

display = WebGraphics(rotate=0)
display.set_pen(display.create_pen(255, 0, 0))
display.rectangle(17, 0, 5, 5)
display.text("0", 17, 0, scale=2)

while True:
    time.sleep(0.02)
