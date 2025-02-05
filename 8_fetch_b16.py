import time
from display_manager import DisplayManager
from bus_graphics import BusGraphics

# Initialize the e-ink display
display_manager = DisplayManager()
display = display_manager.get_display()

# Create MTABusGraphics instance
bus_graphics = MTABusGraphics(display)

while True:
    bus_graphics.fetch_bus_data()
    bus_graphics.update_time()
    bus_graphics.update_display()
    time.sleep(60)  # Refresh every minute
