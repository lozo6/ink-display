# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example queries the Open Weather Maps site API to find out the current
weather for your location... and display it on a eInk Bonnet!
"""

import time
import urllib.request
import urllib.parse
import os
from dotenv import load_dotenv
from display_manager import DisplayManager
from weather_graphics import Weather_Graphics

# Load environment variables
load_dotenv()
OPEN_WEATHER_TOKEN = os.getenv("OPEN_WEATHER_TOKEN")

# Weather API setup
LOCATION = "East Brunswick, US"
DATA_SOURCE_URL = "http://api.openweathermap.org/data/2.5/weather"

if not OPEN_WEATHER_TOKEN:
    raise RuntimeError(
        "You need to set your OPEN_WEATHER_TOKEN in .env. Register at https://home.openweathermap.org/users/sign_up"
    )

params = {"q": LOCATION, "appid": OPEN_WEATHER_TOKEN}
data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(params)

# Initialize the e-ink display
display_manager = DisplayManager()
display = display_manager.get_display()

# Initialize Weather Graphics
gfx = Weather_Graphics(display, am_pm=True, celsius=False)
weather_refresh = None

while True:
    # Query weather every 10 minutes
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 600:
        response = urllib.request.urlopen(data_source)
        if response.getcode() == 200:
            weather_data = response.read()
            print("Weather Response:", weather_data)
            gfx.display_weather(weather_data)
            weather_refresh = time.monotonic()
        else:
            print("Failed to retrieve weather data")

    gfx.update_time()
    time.sleep(300)  # Update time every 5 minutes
