import os
import time
import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
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

# Clear display
display.fill(1)
display.display()

# Function to fetch stock data
import requests

def get_stock_price(symbol):
    API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"

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


# Function to display stock data
def display_stock(symbol):
    stock_symbol, price, change_percent = get_stock_price(symbol)

    if stock_symbol:

        display.rotation = 3

        image = Image.new("1", (display.width, display.height), 255).convert("L")
        draw = ImageDraw.Draw(image)

        # Load font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)

        # Draw stock information on e-paper
        draw.text((10, 10), f"{stock_symbol}", font=font, fill=0)
        draw.text((10, 40), f"Price: ${price:.2f}", font=font, fill=0)
        draw.text((10, 70), f"Change: {change_percent:.2f}%", font=font, fill=0)

        # Display on e-ink
        display.image(image)
        display.display()
    else:
        print("Failed to fetch stock data.")

# Run the script with a stock symbol
stock_ticker = "AAPL"  # Change to your preferred stock
display_stock(stock_ticker)
