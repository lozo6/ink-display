import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Constants
API_URL = "http://bustime.mta.info/api/siri/stop-monitoring.json"
API_KEY = os.getenv(
    "MTA_BUS_TOKEN"
)  # Using os to get the MTA_BUS_TOKEN from the environment
STOP_ID = "301623"  # Stop ID for which you want to fetch data


def fetch_bus_data(api_url: str, api_key: str, stop_id: str) -> dict:
    """Fetch data from the MTA Bus Time API."""
    params = {
        "key": api_key,
        "MonitoringRef": stop_id,
        "version": "2",
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bus time data: {e}")
        exit(1)


def get_monitored_stop_visits(data: dict) -> list:
    """Extract monitored stop visits from the API response."""
    try:
        stop_monitoring_delivery = data["Siri"]["ServiceDelivery"][
            "StopMonitoringDelivery"
        ]
        return stop_monitoring_delivery[0].get("MonitoredStopVisit", [])
    except KeyError:
        print("Error parsing bus time data: Missing expected keys")
        exit(1)


def find_closest_arrival(
    monitored_stop_visits: list, current_time: datetime
) -> datetime:
    """Find the closest arrival time from the list of monitored stop visits."""
    closest_arrival = None

    for visit in monitored_stop_visits:
        expected_arrival_time = (
            visit.get("MonitoredVehicleJourney", {})
            .get("MonitoredCall", {})
            .get("ExpectedArrivalTime")
        )

        if not expected_arrival_time:
            continue  # Skip if arrival time is missing

        # Normalize invalid ISO format (fix "-05:000" to "-05:00")
        normalized_time = expected_arrival_time.replace("-05:000", "-05:00")
        arrival_time = datetime.fromisoformat(normalized_time)  # Parse with timezone

        # Check if the arrival time is after the current time
        if arrival_time > current_time and (
            closest_arrival is None or arrival_time < closest_arrival
        ):
            closest_arrival = arrival_time

    return closest_arrival


def display_arrival_time(closest_arrival: datetime):
    """Display the next bus arrival time."""
    print("Next B16 Arrival Time")
    if closest_arrival:
        print(closest_arrival.strftime("%I:%M %p"))  # Format as HH:MM AM/PM
    else:
        print("No upcoming buses found.")


def main():
    # Current time for comparison (make it timezone-aware)
    current_time = datetime.now(timezone.utc)

    # Fetch bus data and extract monitored stop visits
    bus_data = fetch_bus_data(API_URL, API_KEY, STOP_ID)
    monitored_stop_visits = get_monitored_stop_visits(bus_data)

    # Find the closest arrival time
    closest_arrival = find_closest_arrival(monitored_stop_visits, current_time)

    # Display the closest arrival time
    display_arrival_time(closest_arrival)


if __name__ == "__main__":
    main()
