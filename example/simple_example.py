import displayio
from circuitpython_NV3030B import NV3030B
import board

clk = board.GP10 # change to your board's SPI clock pin
mosi = board.GP11 # change to your board's SPI MOSI pin
cs = board.GP13 # change to your board's SPI CS pin
dc = board.GP12 # change to your board's DC pin
rst = board.GP14 # change to your board's RST pin

display = NV3030B(
    clk, mosi, cs, dc, rst,
    width=240, height=300,
    colstart=0, rowstart=0
)

# instantiate the display canvas
splash = displayio.Group()
display.root_group = splash

# Create a Bitmap
bitmap = displayio.Bitmap(240, 300, 2)

# Create a Palette
palette = displayio.Palette(2)

# Set the colors in the palette
palette[0] = 0xFF0000 # Red

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Add the Group to the Display
splash.append(tile_grid)