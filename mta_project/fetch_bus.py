import requests
from datetime import datetime, timezone


# Constants
API_URL = "http://bustime.mta.info/api/siri/stop-monitoring.json"
API_KEY = "58ae295a-cdaf-4fd5-ab93-8ae0f450b7cc"
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


def find_closest_arrival(data: dict, current_time: datetime) -> datetime:
    """Find the closest arrival time from the fetched bus data."""
    closest_arrival = None

    try:
        monitored_stop_visits = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]

        for visit in monitored_stop_visits:
            monitored_vehicle = visit["MonitoredVehicleJourney"]
            monitored_call = monitored_vehicle.get("MonitoredCall", {})

            # Check if ExpectedArrivalTime exists
            expected_arrival_time = monitored_call.get("ExpectedArrivalTime")
            if not expected_arrival_time:
                continue  # Skip if arrival time is missing

            # Normalize invalid ISO format (fix "-05:000" to "-05:00")
            normalized_time = expected_arrival_time.replace("-05:000", "-05:00")
            arrival_time = datetime.fromisoformat(normalized_time)  # Parse with timezone

            # Check if the arrival time is after the current time
            if arrival_time > current_time:
                if closest_arrival is None or arrival_time < closest_arrival:
                    closest_arrival = arrival_time

        return closest_arrival

    except KeyError as e:
        print(f"Error parsing bus time data: Missing key {e}")
        exit(1)


def display_arrival_time(closest_arrival: datetime):
    """Display the next bus arrival time."""
    print("Next B16 Arrival Time")
    if closest_arrival:
        print(closest_arrival.strftime('%I:%M %p'))  # Format as HH:MM AM/PM
    else:
        print("No upcoming buses found.")


def main():
    # Current time for comparison (make it timezone-aware)
    current_time = datetime.now(timezone.utc)

    # Fetch bus data
    data = fetch_bus_data(API_URL, API_KEY, STOP_ID)

    # Find the closest arrival time
    closest_arrival = find_closest_arrival(data, current_time)

    # Display the closest arrival time
    display_arrival_time(closest_arrival)


if __name__ == "__main__":
    main()
