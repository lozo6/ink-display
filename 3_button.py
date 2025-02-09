import busio
import board
from digitalio import DigitalInOut, Direction
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = DigitalInOut(board.CE0)
dc = DigitalInOut(board.D22)
rst = DigitalInOut(board.D27)
busy = DigitalInOut(board.D17)
srcs = None

display = Adafruit_SSD1680Z(
    122,
    250,
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy,
)

up_button = DigitalInOut(board.D5)
up_button.direction = Direction.INPUT
down_button = DigitalInOut(board.D6)
down_button.direction = Direction.INPUT

while True:
    if not up_button.value:
        print("D5 Button Pressed")

    if not down_button.value:
        print("D6 Button Pressed")
