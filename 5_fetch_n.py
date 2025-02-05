import time
import digitalio
import busio
import board
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z
from subway_graphics import Subway_Graphics

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

# Initialize the Display
display = Adafruit_SSD1680Z(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)

display.rotation = 3

subway_graphics = Subway_Graphics(display)

while True:
    subway_graphics.fetch_subway_data()
    subway_graphics.update_time()
    subway_graphics.update_display()
    time.sleep(60)  # Refresh every minute
