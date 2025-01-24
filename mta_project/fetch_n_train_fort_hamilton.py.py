import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime

# API URL for the GTFS feed
url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"

# Fetch the GTFS feed
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch feed: {e}")
    exit(1)

# Parse the GTFS feed
feed = gtfs_realtime_pb2.FeedMessage()
try:
    feed.ParseFromString(response.content)
except Exception as e:
    print(f"Failed to parse GTFS feed: {e}")
    exit(1)

# Define stop ID for Fort Hamilton Parkway (northbound) and the route ID for the N train
FORT_HAMILTON_STOP_ID = "N03N"  # Stop ID for northbound N train at Fort Hamilton
TARGET_ROUTE_ID = "N"

# Current time for comparison
current_time = datetime.now()

# Initialize variable to track the closest arrival time
closest_arrival = None

# Decode and filter trip updates for the N train at Fort Hamilton (northbound)
for entity in feed.entity:
    if entity.HasField("trip_update"):
        trip = entity.trip_update.trip
        if trip.route_id == TARGET_ROUTE_ID:  # Check for N train
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == FORT_HAMILTON_STOP_ID:  # Check for Fort Hamilton northbound
                    arrival_time = datetime.fromtimestamp(stop_time_update.arrival.time)

                    # Check if the arrival time is after the current time
                    if arrival_time > current_time:
                        # Update the closest arrival
                        if closest_arrival is None or arrival_time < closest_arrival:
                            closest_arrival = arrival_time

# Display the formatted output
print("N Train")
print("Fort Hamilton Station")
if closest_arrival:
    print(f"Arrival Time: {closest_arrival.strftime('%I:%M %p')}")  # Format as HH:MM AM/PM
else:
    print("Arrival Time: No upcoming trains")
