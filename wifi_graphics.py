# SPDX-FileCopyrightText: 2024 Your Name
# SPDX-License-Identifier: MIT

import qrcode
from PIL import Image, ImageDraw, ImageFont
import adafruit_epd.epd as epd
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z

class Wifi_Graphics:
    """Handles QR code generation and display for WiFi credentials on e-ink display."""

    def __init__(self, display):
        self.display = display
        self.image = Image.new("1", (display.width, display.height), 255).convert("L")
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()

    def generate_qr(self, ssid, password, auth):
        """Generates a WiFi QR code based on credentials."""
        wifi_qr_data = f"WIFI:S:{ssid};T:{auth};P:{password};;"
        qr = qrcode.make(wifi_qr_data)
        qr = qr.resize((100, 100), Image.Resampling.LANCZOS)  # Resize for e-ink
        return qr

    def display_qr(self, ssid, password, auth):
        """Displays the generated QR code on the e-ink display."""
        qr = self.generate_qr(ssid, password, auth)
        self.image.paste(qr, (75, 10))

        # Add label text
        self.draw.text((10, 120), "Scan to Connect", font=self.font, fill=0)

        # Update e-ink display
        self.display.image(self.image)
        self.display.display()
        print("WiFi QR Code displayed!")
