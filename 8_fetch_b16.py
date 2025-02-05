import time
import os
from dotenv import load_dotenv
from display_manager import DisplayManager
from bus_graphics import BusGraphics

# Load environment variables
load_dotenv()
MTA_BUS_TOKEN = os.getenv("MTA_BUS_TOKEN")

# Initialize the e-ink display
display_manager = DisplayManager()
display = display_manager.get_display()

# Create BusGraphics instance with API key
bus_graphics = BusGraphics(display, MTA_BUS_TOKEN)

while True:
    bus_graphics.fetch_bus_data()
    bus_graphics.update_time()
    bus_graphics.update_display()
    time.sleep(60)  # Refresh every minute
