# SPDX-FileCopyrightText: 2024 Your Name
# SPDX-License-Identifier: MIT

import os
import time
from dotenv import load_dotenv
from display_manager import DisplayManager
from stock_graphics import Stock_Graphics

# Load environment variables
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# Initialize the e-ink display
display_manager = DisplayManager()
display = display_manager.get_display()

# Create Stock_Graphics instance
gfx = Stock_Graphics(display, ALPHA_VANTAGE_API_KEY)

while True:
    stock_ticker = "NVDA"  # Change to preferred stock symbol
    gfx.display_stock(stock_ticker)
    time.sleep(300)  # Refresh every 10 minutes
