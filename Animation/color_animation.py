# This script supports the Raspberry Pi Pico board and the Lilygo ESP32-S2 board
# Color OLED Display: http://educ8s.tv/part/ColorOLED
# Raspberry Pi Pico: http://educ8s.tv/part/RaspberryPiPico
# ESP32-S2 Board: http://educ8s.tv/part/esp32s2

import board, busio, displayio, os, time
from adafruit_ssd1331 import SSD1331
import adafruit_imageload

IMAGE_FILE = "icon.bmp"
FRAMES = 28

displayio.release_displays()

board_type = os.uname().machine
print(f"Board: {board_type}")

if 'Pico' in board_type:
    clk_pin, mosi_pin, reset_pin, dc_pin, cs_pin = board.GP18, board.GP19, board.GP16, board.GP20, board.GP17
elif 'ESP32-S2' in board_type:
    mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.IO35, board.IO36, board.IO38, board.IO34, board.IO37    
else:
    mosi_pin, clk_pin, reset_pin, cs_pin, dc_pin = board.GP11, board.GP10, board.GP17, board.GP18, board.GP16
    print("This board is not supported. Change the pin definitions above.")

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = SSD1331(display_bus, width=96, height=64)

group = displayio.Group()

color_bitmap = displayio.Bitmap(96, 64, 1)

color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
group.append(bg_sprite)

#  load the spritesheet
icon_bit, icon_pal = adafruit_imageload.load(IMAGE_FILE,
                                                 bitmap=displayio.Bitmap,
                                                 palette=displayio.Palette)

icon_grid = displayio.TileGrid(icon_bit, pixel_shader=icon_pal,
                                 width=1, height=1,
                                 tile_height=50, tile_width=50,
                                 default_tile=0,
                                 x=23, y=7)

group.append(icon_grid)

display.show(group)

timer = 0
pointer = 0

while True:
  if (timer + 0.1) < time.monotonic():
    icon_grid[0] = pointer
    pointer += 1
    timer = time.monotonic()
    if pointer > FRAMES-1:
      pointer = 0