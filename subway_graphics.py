from datetime import datetime
import os
import requests
from google.transit import gtfs_realtime_pb2
from PIL import Image, ImageDraw, ImageFont

# Load fonts
small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
)

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Subway_Graphics:
    """Fetches and displays subway arrival times on an e-ink display."""

    def __init__(self, display):
        self.display = display
        self.api_url = os.getenv(
            "MTA_GTFS_URL",
            "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw",
        )

        # Initialize subway info placeholders
        self._subway_name = "N Subway"
        self._station_name = "Fort Hamilton Station"
        self._arrival_time = "Loading..."
        self._time_text = None

    def fetch_gtfs_feed(self):
        """Fetches GTFS data from MTA API and returns parsed data."""
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            return feed
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch GTFS feed: {e}")
            return None

    def fetch_subway_data(self):
        """Extracts the next subway arrival time from GTFS feed."""
        feed = self.fetch_gtfs_feed()
        if not feed:
            self._arrival_time = "No data available"
            return

        FORT_HAMILTON_STOP_ID = (
            "N03N"  # Stop ID for northbound N subway at Fort Hamilton
        )
        TARGET_ROUTE_ID = "N"

        current_time = datetime.now()
        closest_arrival = None

        for entity in feed.entity:
            if entity.HasField("trip_update"):
                trip = entity.trip_update.trip
                if trip.route_id == TARGET_ROUTE_ID:
                    for stop_time_update in entity.trip_update.stop_time_update:
                        if stop_time_update.stop_id == FORT_HAMILTON_STOP_ID:
                            arrival_time = datetime.fromtimestamp(
                                stop_time_update.arrival.time
                            )

                            if arrival_time > current_time:
                                if (
                                    closest_arrival is None
                                    or arrival_time < closest_arrival
                                ):
                                    closest_arrival = arrival_time

        self._arrival_time = (
            closest_arrival.strftime("%I:%M %p")
            if closest_arrival
            else "No upcoming subways"
        )

    def update_time(self):
        """Updates the current time display."""
        now = datetime.now()
        self._time_text = now.strftime(
            "%I:%M %p").lstrip("0").replace(" 0", " ")

    def update_display(self):
        """Updates the e-ink display with subway data."""
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width,
                          self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Display text
        draw.text((5, 5), self._subway_name, font=medium_font, fill=BLACK)
        draw.text((5, 25), self._station_name, font=small_font, fill=BLACK)
        draw.text(
            (5, 50), f"Arrival: {self._arrival_time}", font=large_font, fill=BLACK
        )

        # Draw current time at bottom right
        font_width, font_height = medium_font.getsize(self._time_text)
        draw.text(
            (
                self.display.width - font_width - 5,
                self.display.height - font_height - 5,
            ),
            self._time_text,
            font=medium_font,
            fill=BLACK,
        )

        self.display.image(image)
        self.display.display()
