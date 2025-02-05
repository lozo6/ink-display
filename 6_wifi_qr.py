# SPDX-FileCopyrightText: 2024 Your Name
# SPDX-License-Identifier: MIT

import os
from dotenv import load_dotenv
from display_manager import DisplayManager
from wifi_graphics import Wifi_Graphics

# Load environment variables
load_dotenv()

# Load WiFi credentials
WIFI_SSID = os.getenv("WIFI_SSID", "Your_SSID")
WIFI_PASSWORD = os.getenv("WIFI_PASSWORD", "Your_Password")
WIFI_AUTH = os.getenv("WIFI_AUTH", "WPA")  # Options: WEP, WPA, nopass

# Initialize the e-ink display
display_manager = DisplayManager()
display = display_manager.get_display()

# Create Wifi_Graphics instance and display QR code
gfx = Wifi_Graphics(display)
gfx.display_qr(WIFI_SSID, WIFI_PASSWORD, WIFI_AUTH)
