import time
import requests
from PIL import Image, ImageDraw, ImageFont
import adafruit_epd.epd as epd
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z
import board
import busio
import digitalio

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
def get_stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error if request fails
        data = response.json()

        if "quoteResponse" in data and "result" in data["quoteResponse"] and data["quoteResponse"]["result"]:
            stock = data["quoteResponse"]["result"][0]
            return stock.get("symbol"), stock.get("regularMarketPrice", 0), stock.get("regularMarketChangePercent", 0)
    except (requests.RequestException, KeyError, IndexError):
        print("Failed to fetch stock data.")
    return None, None, None


# Function to display stock data
def display_stock(symbol):
    stock_symbol, price, change_percent = get_stock_price(symbol)

    if stock_symbol:
        # Create an image buffer for the SSD1680Z
        image = Image.new("1", (display.width, display.height), 255)
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
