from datetime import datetime
import requests
from google.transit import gtfs_realtime_pb2
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
)

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Train_Graphics:
    def __init__(self, display):
        self.display = display

        self._train_name = None
        self._station_name = None
        self._arrival_time = None
        self._time_text = None

    def fetch_train_data(self):
        url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch feed: {e}")
            return

        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            feed.ParseFromString(response.content)
        except Exception as e:
            print(f"Failed to parse GTFS feed: {e}")
            return

        FORT_HAMILTON_STOP_ID = "N03N"  # Stop ID for northbound N train at Fort Hamilton
        TARGET_ROUTE_ID = "N"  # Route ID for the N train

        current_time = datetime.now()

        closest_arrival = None

        for entity in feed.entity:
            if entity.HasField("trip_update"):
                trip = entity.trip_update.trip
                if trip.route_id == TARGET_ROUTE_ID:
                    for stop_time_update in entity.trip_update.stop_time_update:
                        if stop_time_update.stop_id == FORT_HAMILTON_STOP_ID:
                            arrival_time = datetime.fromtimestamp(stop_time_update.arrival.time)

                            if arrival_time > current_time:
                                if closest_arrival is None or arrival_time < closest_arrival:
                                    closest_arrival = arrival_time

        if closest_arrival:
            self._train_name = "N Train"
            self._station_name = "Fort Hamilton Station"
            self._arrival_time = closest_arrival.strftime('%I:%M %p')
        else:
            self._train_name = "N Train"
            self._station_name = "Fort Hamilton Station"
            self._arrival_time = "No upcoming trains"

    def update_time(self):
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    def update_display(self):
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the train name
        draw.text((5, 5), self._train_name, font=medium_font, fill=BLACK)

        # Draw the station name
        draw.text((5, 25), self._station_name, font=small_font, fill=BLACK)

        # Draw the arrival time
        draw.text((5, 50), f"Arrival: {self._arrival_time}", font=large_font, fill=BLACK)

        # Draw the time
        (font_width, font_height) = medium_font.getsize(self._time_text)
        draw.text(
            (self.display.width - font_width - 5, self.display.height - font_height - 5),
            self._time_text,
            font=medium_font,
            fill=BLACK,
        )

        self.display.image(image)
        self.display.display()
