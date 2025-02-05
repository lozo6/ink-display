import board
import busio
import digitalio
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z


class DisplayManager:
    """Manages SPI and e-ink display initialization for all modules."""

    def __init__(self, rotation=3):
        # Configure SPI and EPD pins
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.ecs = digitalio.DigitalInOut(board.CE0)
        self.dc = digitalio.DigitalInOut(board.D22)
        self.rst = digitalio.DigitalInOut(board.D27)
        self.busy = digitalio.DigitalInOut(board.D17)

        # Initialize the e-ink display
        self.display = Adafruit_SSD1680Z(
            122,
            250,
            self.spi,
            cs_pin=self.ecs,
            dc_pin=self.dc,
            sramcs_pin=None,
            rst_pin=self.rst,
            busy_pin=self.busy,
        )
        self.display.rotation = rotation

    def get_display(self):
        """Returns the initialized display instance."""
        return self.display
