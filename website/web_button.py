BUTTON_STATES = {
    "a": False,
    "b": False,
    "x": False,
    "y": False,
}


class WebButton:
    def __init__(self, name):
        self.name = name

    def read(self):
        return BUTTON_STATES.get(self.name, False)
