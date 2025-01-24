import requests
from datetime import datetime, timezone

# MTA Bus Time API URL and your API key
API_URL = "http://bustime.mta.info/api/siri/stop-monitoring.json"
API_KEY = "58ae295a-cdaf-4fd5-ab93-8ae0f450b7cc"
STOP_ID = "301623"  # Stop ID for which you want to fetch data

# Parameters for the API request
params = {
    "key": API_KEY,
    "MonitoringRef": STOP_ID,
    "version": "2",
}

# Fetch data from the API
try:
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching bus time data: {e}")
    exit(1)

# Current time for comparison (make it timezone-aware)
current_time = datetime.now(timezone.utc)

# Initialize variable for closest arrival time
closest_arrival = None

# Extract and find the closest arrival time
try:
    monitored_stop_visits = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]

    for visit in monitored_stop_visits:
        monitored_vehicle = visit["MonitoredVehicleJourney"]
        monitored_call = monitored_vehicle.get("MonitoredCall", {})

        # Check if ExpectedArrivalTime exists
        expected_arrival_time = monitored_call.get("ExpectedArrivalTime")
        if not expected_arrival_time:
            continue  # Skip this bus if arrival time is missing

        # Fix invalid ISO format (correct -05:000 to -05:00)
        normalized_time = expected_arrival_time.replace("-05:000", "-05:00")
        arrival_time = datetime.fromisoformat(normalized_time)  # Parse with timezone

        # Check if the arrival time is after the current time
        if arrival_time > current_time:
            # Update the closest arrival time
            if closest_arrival is None or arrival_time < closest_arrival:
                closest_arrival = arrival_time

    # Display the closest arrival time
    print("Next B16 Arrival Time")
    if closest_arrival:
        print(closest_arrival.strftime('%I:%M %p'))  # Format as HH:MM AM/PM
    else:
        print("No upcoming buses found.")
except KeyError as e:
    print(f"Error parsing bus time data: Missing key {e}")
