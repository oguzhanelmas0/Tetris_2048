import lib.stddraw as stddraw  
from lib.color import Color  

class Tile:
    boundary_thickness = 0.004
    font_family, font_size = "Arial", 16

    _BG_COLORS = {
        2: Color(238, 228, 218),
        4: Color(237, 224, 200),
        8: Color(242, 177, 121),
        16: Color(245, 149, 99),
        32: Color(246, 124, 95),
        64: Color(246, 94, 59),
        128: Color(237, 207, 114),
        256: Color(237, 204, 97),
        512: Color(237, 200, 80),
        1024: Color(237, 197, 63),
        2048: Color(237, 194, 46),
        4096: Color(60, 58, 50)
    }

    _FG_DARK = Color(119, 110, 101)
    _FG_LIGHT = Color(249, 246, 242)
    _BOX_COLOR = Color(187, 173, 160)

    def __init__(self):
        self.number = 2
        self.background_color = Tile._BG_COLORS.get(2)
        self.foreground_color = Tile._FG_DARK
        self.box_color = Tile._BOX_COLOR
        self.is_connected = False

    def draw(self, position, length=1):

        self.background_color = Tile._BG_COLORS.get(self.number, Color(60, 58, 50))
        self.foreground_color = Tile._FG_DARK if self.number <= 4 else Tile._FG_LIGHT


        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)


        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()


        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))
