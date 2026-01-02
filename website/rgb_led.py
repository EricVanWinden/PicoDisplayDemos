import logging


class RGBLED:
    def __init__(self, v1, v2, v3):
        logging.info(f"Initializing RGB LED {v1},{v2},{v3}")

    def set_rgb(self, r, g, b):
        logging.info(f"Setting RGB to {r},{g},{b}")
