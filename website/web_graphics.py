DRAW_COMMANDS = []


class WebGraphics:
    def __init__(self, display=None, rotate=0):
        self.current_pen = (255, 255, 255)
        self.rotate = rotate

        # Pico Display resolution
        self.width = 240
        self.height = 135

        # Swap dimensions if rotated 90 or 270
        if rotate in (90, 270):
            self.width, self.height = self.height, self.width

    def _transform(self, x, y, w=0, h=0):
        """Apply rotation transform to coordinates."""
        if self.rotate == 0:
            return x, y, w, h

        elif self.rotate == 90:
            # (x, y) -> (height - y - h, x)
            return (self.height - y - h, x, h, w)

        elif self.rotate == 180:
            # (x, y) -> (width - x - w, height - y - h)
            return (self.width - x - w, self.height - y - h, w, h)

        elif self.rotate == 270:
            # (x, y) -> (y, width - x - w)
            return (y, self.width - x - w, h, w)

        return x, y, w, h

    def set_backlight(self, value):
        pass

    def create_pen(self, r, g, b):
        return (r, g, b)

    def set_pen(self, pen):
        self.current_pen = pen

    def clear(self):
        DRAW_COMMANDS.clear()
        DRAW_COMMANDS.append({"cmd": "clear"})

    def rectangle(self, x, y, w, h):
        tx, ty, tw, th = self._transform(x, y, w, h)
        DRAW_COMMANDS.append({
            "cmd": "rect",
            "x": tx,
            "y": ty,
            "w": tw,
            "h": th,
            "color": self.current_pen
        })

    def text(self, message, x, y, scale=1):
        tx, ty, _, _ = self._transform(x, y)
        DRAW_COMMANDS.append({
            "cmd": "text",
            "text": message,
            "x": tx,
            "y": ty,
            "scale": scale,
            "color": self.current_pen
        })

    def update(self):
        pass
