import time
from display_manager import DisplayManager
from subway_graphics import Subway_Graphics

# Initialize the e-ink display
display_manager = DisplayManager()
display = display_manager.get_display()

# Create Subway_Graphics instance
subway_graphics = Subway_Graphics(display)

while True:
    subway_graphics.fetch_subway_data()
    subway_graphics.update_time()
    subway_graphics.update_display()
    time.sleep(60)  # Refresh every minute
