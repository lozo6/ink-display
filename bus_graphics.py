import os
import requests
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

# Load fonts
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class BusGraphics:
    """Fetches and displays MTA bus arrival times on an e-ink display."""

    def __init__(self, display):
        self.display = display
        self.api_url = "http://bustime.mta.info/api/siri/stop-monitoring.json"
        self.api_key = os.getenv("MTA_BUS_TOKEN")
        self.stop_id = "301623"
        self._bus_name = "B16 Bus"
        self._arrival_time = "Loading..."
        self._time_text = None

    def fetch_bus_data(self):
        """Fetches bus arrival data from the MTA Bus Time API."""
        params = {"key": self.api_key, "MonitoringRef": self.stop_id, "version": "2"}
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            self.process_bus_data(data)
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                print("Error 401: Unauthorized - Check your API key.")
            elif response.status_code == 403:
                print("Error 403: Forbidden - API key may not have access.")
            else:
                print(f"HTTP Error: {e}")
            self._arrival_time = "No data available"
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch bus data: {e}")
            self._arrival_time = "No data available"

    def process_bus_data(self, data):
        """Processes bus API response and finds the next arrival time."""
        try:
            stop_monitoring = data["Siri"]["ServiceDelivery"].get("StopMonitoringDelivery", [{}])[0]
            monitored_stop_visits = stop_monitoring.get("MonitoredStopVisit", [])
            closest_arrival = None
            current_time = datetime.now(timezone.utc)

            for visit in monitored_stop_visits:
                expected_time = visit.get("MonitoredVehicleJourney", {}).get("MonitoredCall", {}).get("ExpectedArrivalTime")
                if not expected_time:
                    continue
                arrival_time = datetime.fromisoformat(expected_time.replace("-05:000", "-05:00"))
                if arrival_time > current_time and (closest_arrival is None or arrival_time < closest_arrival):
                    closest_arrival = arrival_time

            self._arrival_time = closest_arrival.strftime('%I:%M %p') if closest_arrival else "No upcoming buses"
        except (KeyError, IndexError):
            self._arrival_time = "Parsing error"

    def update_time(self):
        """Updates the current time display."""
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    def update_display(self):
        """Updates the e-ink display with bus data."""
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        draw.text((5, 5), self._bus_name, font=medium_font, fill=BLACK)
        draw.text((5, 30), f"Arrival: {self._arrival_time}", font=large_font, fill=BLACK)

        font_width, font_height = medium_font.getsize(self._time_text)
        draw.text((self.display.width - font_width - 5, self.display.height - font_height - 5), self._time_text, font=medium_font, fill=BLACK)

        self.display.image(image)
        self.display.display()
