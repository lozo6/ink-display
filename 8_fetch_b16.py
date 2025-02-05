import time
from dotenv import load_dotenv
from display_manager import DisplayManager
from bus_graphics import BusGraphics

# Load environment variables
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# Initialize the e-ink display
display_manager = DisplayManager()
display = display_manager.get_display()

# Create BusGraphics instance
bus_graphics = BusGraphics(display)

while True:
    bus_graphics.fetch_bus_data()
    bus_graphics.update_time()
    bus_graphics.update_display()
    time.sleep(60)  # Refresh every minute
