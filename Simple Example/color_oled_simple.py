# This script supports the Raspberry Pi Pico board and the Lilygo ESP32-S2 board
# Color OLED Display: http://educ8s.tv/part/ColorOLED
# Raspberry Pi Pico: http://educ8s.tv/part/RaspberryPiPico
# ESP32-S2 Board: http://educ8s.tv/part/esp32s2


import board, busio, displayio, os
import terminalio #Just a font
from adafruit_ssd1331 import SSD1331
from adafruit_display_text import label

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

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(96, 64, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(86, 54, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=5)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=12, y=32)
splash.append(text_area)

while True:
    pass