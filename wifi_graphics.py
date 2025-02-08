import qrcode
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)


class Wifi_Graphics:
    """Handles QR code generation and display for WiFi credentials on e-ink display."""

    def __init__(self, display):
        self.display = display
        self.image = Image.new(
            "1", (display.width, display.height), 255).convert("L")
        self.draw = ImageDraw.Draw(self.image)

    def generate_qr(self, ssid, password, auth):
        """Generates a WiFi QR code based on credentials."""
        wifi_qr_data = f"WIFI:S:{ssid};T:{auth};P:{password};;"
        qr = qrcode.make(wifi_qr_data)
        # Resize for e-ink
        qr = qr.resize((140, 140), Image.Resampling.LANCZOS)
        return qr

    def display_qr(self, ssid, password, auth):
        """Displays the generated QR code on the e-ink display."""
        qr = self.generate_qr(ssid, password, auth)

        self.draw.text((10, 30), "Connect to", font=font, fill=0)
        self.draw.text((10, 50), "Pransisko98:", font=font, fill=0)

        self.image.paste(qr, (120, -10))

        # Update e-ink display
        self.display.image(self.image)
        self.display.display()
