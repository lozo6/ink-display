# main.py
import requests
import os
import digitalio
import busio
import board
import time
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from dotenv import load_dotenv
from mta_graphics import MTAGraphics  # Renamed class

# Load the environment variable
load_dotenv()

# SPI and eInk display setup
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input()
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input()

DEBOUNCE_DELAY = 0.3

# Station and API configurations
station_codes = ["N03N"]  # Only Fort Hamilton northbound
station_code_index = 0

api_key = os.getenv("MTA_API_KEY")  # Replace with your MTA API key
api_url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"
headers = {"x-api-key": api_key}

# Initialize the eInk display
display = Adafruit_SSD1675(
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy
)
display.rotation = 1
gfx = MTAGraphics(display)
refresh_display = None

def fetch_next_train():
    """
    Fetch the next train arrival for the current station.
    """
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.content
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return "Error", "N/A", "N/A"

    # Parse GTFS data
    from google.transit import gtfs_realtime_pb2
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)

    current_time = time.time()
    closest_arrival = None
    closest_minutes = None

    # Find the next train arrival for the station
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            trip = entity.trip_update.trip
            if trip.route_id == "N":  # N Train
                for stop_time_update in entity.trip_update.stop_time_update:
                    if stop_time_update.stop_id == station_codes[station_code_index]:
                        arrival_time = stop_time_update.arrival.time
                        if arrival_time > current_time:
                            if not closest_arrival or arrival_time < closest_arrival:
                                closest_arrival = arrival_time
                                closest_minutes = int((arrival_time - current_time) / 60)

    if closest_arrival:
        arrival_time_str = time.strftime("%I:%M %p", time.localtime(closest_arrival))
        return arrival_time_str, closest_minutes
    return "No Trains", "N/A"

while True:
    # Refresh display every 60 seconds
    if not refresh_display or (time.monotonic() - refresh_display) > 60:
        arrival_time, arrival_minutes = fetch_next_train()
        gfx.update_metro("Fort Hamilton", "N Train", arrival_time, arrival_minutes)
        refresh_display = time.monotonic()

    # Button handling to cycle stations (if more stations are added)
    if up_button.value != down_button.value:
        if not up_button.value and station_code_index < len(station_codes) - 1:
            station_code_index += 1
        else:
            station_code_index = 0
        time.sleep(DEBOUNCE_DELAY)

        # Fetch and display the next train for the updated station
        arrival_time, arrival_minutes = fetch_next_train()
        gfx.update_metro("Fort Hamilton", "N Train", arrival_time, arrival_minutes)

    # Update the clock
    gfx.update_time()
