# SPDX-FileCopyrightText: 2024 Your Name
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import board
import busio
import digitalio
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z
from wifi_graphics import Wifi_Graphics

# Load environment variables
load_dotenv()

# Configure SPI and EPD pins
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

# Initialize the e-ink display
display = Adafruit_SSD1680Z(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy)
display.rotation = 3

# Load WiFi credentials
WIFI_SSID = os.getenv("WIFI_SSID", "Your_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD", "Your_Password")
WIFI_AUTH = os.getenv("WIFI_AUTH", "WPA")  # Options: WEP, WPA, nopass

# Create Wifi_Graphics instance and display QR code
gfx = Wifi_Graphics(display)
gfx.display_qr(WIFI_SSID, WIFI_PASSWORD, WIFI_AUTH)
