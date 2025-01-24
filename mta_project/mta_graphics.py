# mta_graphics.py
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

# Font configuration
small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
)

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class MTAGraphics:
    def __init__(self, display):
        # Initialize fonts, display, and attributes
        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font
        self.display = display

        self._station_name = None
        self._train_line = None
        self._arrival_time = None
        self._arrival_minutes = None

    def update_metro(self, station_name, train_line, arrival_time, arrival_minutes):
        """
        Update the train data to be displayed.
        """
        self._station_name = station_name
        self._train_line = train_line
        self._arrival_time = arrival_time
        self._arrival_minutes = arrival_minutes

        self.update_time()
        self.update_display()

    def update_time(self):
        """
        Update the current time for display.
        """
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    def update_display(self):
        """
        Render the updated train information on the e-ink display.
        """
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the station name
        draw.text((5, 5), self._station_name, font=self.large_font, fill=BLACK)

        # Draw the train line
        draw.text((5, 35), self._train_line, font=self.medium_font, fill=BLACK)

        # Draw the arrival time
        if self._arrival_time:
            draw.text(
                (5, 65),
                f"Time: {self._arrival_time}",
                font=self.medium_font,
                fill=BLACK,
            )

            # Draw the arrival in minutes
            draw.text(
                (5, 95),
                f"In: {self._arrival_minutes} mins",
                font=self.medium_font,
                fill=BLACK,
            )
        else:
            draw.text(
                (5, 65),
                "No upcoming trains",
                font=self.medium_font,
                fill=BLACK,
            )

        # Draw the current time
        draw.text(
            (5, self.display.height - 30),
            f"Now: {self._time_text}",
            font=self.small_font,
            fill=BLACK,
        )

        # Send the image to the e-ink display
        self.display.image(image)
        self.display.display()
