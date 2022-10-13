# This script supports the Raspberry Pi Pico board and the Lilygo ESP32-S2 board
# Color OLED Display: http://educ8s.tv/part/ColorOLED
# Raspberry Pi Pico: http://educ8s.tv/part/RaspberryPiPico
# ESP32-S2 Board: http://educ8s.tv/part/esp32s2

import board, busio, displayio, os, time
import terminalio #Just a font
from adafruit_ssd1331 import SSD1331
from adafruit_display_text import label
from paddle import Paddle
from ball import Ball

SCREEN_WIDTH = 96
SCREEN_HEIGHT = 64

FPS = 120
FPS_DELAY = 1 / FPS

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

display = SSD1331(display_bus, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Make a background color fill
color_bitmap = displayio.Bitmap(SCREEN_WIDTH, SCREEN_HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
splash.append(bg_sprite)

right_paddle = Paddle(3,20,SCREEN_WIDTH-3,int(SCREEN_HEIGHT/2 - 10), 0xFF0000)
splash.append(right_paddle.rect)

left_paddle = Paddle(3,20,0,int(SCREEN_HEIGHT/2 - 10), 0xFFFF00)
splash.append(left_paddle.rect)

ball = Ball(3,10,5)
splash.append(ball.circle)

last_update_time = 0
now = 0
loops_since_update = 0

while True:
    # update time variable
    now = time.monotonic()

    # check if the delay time has passed since the last game update
    if last_update_time + FPS_DELAY <= now:
        
        # update objects
        ball.update(left_paddle, right_paddle )
        left_paddle.update(ball)
        right_paddle.update(ball)
        
        last_update_time = now
        loops_since_update = 0
    else:
        loops_since_update += 1