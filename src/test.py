from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
import time

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY)
display.set_backlight(1.0)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

while True:
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(WHITE)
    display.text("Hello!", 10, 10, scale=3)
    display.update()
    time.sleep(1)
