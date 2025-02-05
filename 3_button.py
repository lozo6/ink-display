import digitalio
import busio
import board
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.D12)
dc = digitalio.DigitalInOut(board.D11)
srcs = digitalio.DigitalInOut(board.D10)  # can be None to use internal memory
rst = digitalio.DigitalInOut(board.D9)  # can be None to not use this pin
busy = digitalio.DigitalInOut(board.D5)  # can be None to not use this pin

display = Adafruit_SSD1680(
    122,
    250,  # 2.13" HD Tri-color or mono display
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy,
)

up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input(pull=digitalio.Pull.UP)  # Use pull-up resistor
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input(pull=digitalio.Pull.UP)  # Use pull-up resistor

while True:
    if not digitalio.DigitalInOut(board.D5).value:
        print("D5 Button Pressed")

    if not digitalio.DigitalInOut(board.D6).value:
        print("D6 Button Pressed")
