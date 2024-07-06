from Frontend import Frontend
from Drawable import Drawable
from PixelData import PixelData

f = Frontend()
f.load_colors()

pd = PixelData()
pd.set_icon("%")
pd.set_cursor(False)

d = Drawable(pd)
d.set_color(1)
d.set_y(10)

d.set_x(10)
d.set_type("background")
f.paint_pixel(d)

d.set_x(11)
d.set_type("unfocused_track")
f.paint_pixel(d)

d.set_x(12)
d.set_type("focused_track")
f.paint_pixel(d)

d.set_x(13)
d.set_cursor(True)
f.paint_pixel(d)

f.s.getch()

f.close()
