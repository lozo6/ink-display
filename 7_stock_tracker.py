# SPDX-FileCopyrightText: 2024 Your Name
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
import board
import busio
import digitalio
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z
from stock_graphics import Stock_Graphics

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

# Load API Key
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# Create Stock_Graphics instance and display stock data
while True:
    gfx = Stock_Graphics(display, ALPHA_VANTAGE_API_KEY)
    stock_ticker = "NVDA"  # Change this to any stock symbol you want
    gfx.display_stock(stock_ticker)
