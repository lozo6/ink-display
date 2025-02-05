# SPDX-FileCopyrightText: 2024 Your Name
# SPDX-License-Identifier: MIT

import os
import requests
from PIL import Image, ImageDraw, ImageFont
import adafruit_epd.epd as epd
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z

class Stock_Graphics:
    """Fetches and displays stock market data on e-ink display."""

    def __init__(self, display, api_key):
        self.display = display
        self.api_key = api_key
        self.image = Image.new("1", (display.width, display.height), 255).convert("L")
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)

    def get_stock_price(self, symbol):
        """Fetch stock price from Alpha Vantage API."""
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if "Global Quote" in data:
                stock = data["Global Quote"]
                return stock.get("01. symbol"), float(stock.get("05. price", 0)), float(stock.get("10. change percent", "0%").strip('%'))
        except (requests.RequestException, KeyError, IndexError, ValueError):
            print("Failed to fetch stock data.")
        return None, None, None

    def display_stock(self, symbol):
        """Fetch and display stock data on e-ink screen."""
        stock_symbol, price, change_percent = self.get_stock_price(symbol)

        if stock_symbol:
            self.draw.text((10, 10), f"{stock_symbol}", font=self.font, fill=0)
            self.draw.text((10, 40), f"Price: ${price:.2f}", font=self.font, fill=0)
            self.draw.text((10, 70), f"Change: {change_percent:.2f}%", font=self.font, fill=0)

            # Update e-ink display
            self.display.image(self.image)
            self.display.display()
        else:
            print("Failed to fetch stock data.")
