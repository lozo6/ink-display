import os
import qrcode
from dotenv import load_dotenv
from PIL import Image, ImageDraw
import adafruit_epd.epd as epd
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z
import board
import busio
import digitalio

load_dotenv()

# Configure SPI and EPD pins
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

# Initialize the SSD1680Z e-ink display
display = Adafruit_SSD1680Z(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)

# WiFi credentials (Modify these)
WIFI_SSID = os.getenv("WIFI_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")
WIFI_AUTH = os.getenv("WIFI_AUTH")  # Options: WEP, WPA, nopass

display.rotation = 1

# Generate WiFi QR Code using WiFi format
wifi_qr_data = f"WIFI:S:{WIFI_SSID};T:{WIFI_AUTH};P:{WIFI_PASSWORD};;"
qr = qrcode.make(wifi_qr_data)

# Resize QR code to fit SSD1680Z display
qr = qr.resize((100, 100), Image.Resampling.LANCZOS)

# Create an image buffer
image = Image.new("1", (display.width, display.height), 255).convert("L")
draw = ImageDraw.Draw(image)

# Paste QR code onto display
image.paste(qr, (75, 10))

# Display label
draw.text((10, 100), "Scan to Connect", fill=0)

# Display on e-ink
display.image(image)
display.display()

print("WiFi QR Code displayed!")
