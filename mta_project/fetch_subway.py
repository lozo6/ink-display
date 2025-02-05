import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime


# Constants
URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw"
FORT_HAMILTON_STOP_ID = "N03N"  # Stop ID for northbound N train at Fort Hamilton
TARGET_ROUTE_ID = "N"


def fetch_gtfs_feed(url: str) -> gtfs_realtime_pb2.FeedMessage:
    """Fetch and parse the GTFS feed."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch feed: {e}")
        exit(1)
    except Exception as e:
        print(f"Failed to parse GTFS feed: {e}")
        exit(1)


def get_closest_train_arrival(
    feed: gtfs_realtime_pb2.FeedMessage, target_route_id: str, stop_id: str
) -> datetime:
    """Find the closest upcoming train arrival time."""
    current_time = datetime.now()
    closest_arrival = None

    for entity in feed.entity:
        if entity.HasField("trip_update"):
            trip = entity.trip_update.trip
            if trip.route_id == target_route_id:
                for stop_time_update in entity.trip_update.stop_time_update:
                    if stop_time_update.stop_id == stop_id:
                        arrival_time = datetime.fromtimestamp(
                            stop_time_update.arrival.time
                        )

                        # Only consider future arrival times
                        if arrival_time > current_time:
                            if (
                                closest_arrival is None
                                or arrival_time < closest_arrival
                            ):
                                closest_arrival = arrival_time
    return closest_arrival


def display_train_info(closest_arrival: datetime):
    """Display the train information in a readable format."""
    print("N Train")
    print("Fort Hamilton Station")
    if closest_arrival:
        print(
            f"Arrival Time: {closest_arrival.strftime('%I:%M %p')}"
        )  # Format as HH:MM AM/PM
    else:
        print("Arrival Time: No upcoming trains")


def main():
    # Fetch and parse the GTFS feed
    feed = fetch_gtfs_feed(URL)

    # Get the closest train arrival
    closest_arrival = get_closest_train_arrival(
        feed, TARGET_ROUTE_ID, FORT_HAMILTON_STOP_ID
    )

    # Display the train information
    display_train_info(closest_arrival)


if __name__ == "__main__":
    main()
