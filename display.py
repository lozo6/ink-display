# SPDX-FileCopyrightText: 2019 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Image resizing and drawing using the Pillow Library. For the image, check out the
associated Adafruit Learn guide at:
https://learn.adafruit.com/adafruit-eink-display-breakouts/python-code

"""

import digitalio
import busio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.il0373 import Adafruit_IL0373
from adafruit_epd.il91874 import Adafruit_IL91874  # pylint: disable=unused-import
from adafruit_epd.il0398 import Adafruit_IL0398  # pylint: disable=unused-import
from adafruit_epd.ssd1608 import Adafruit_SSD1608  # pylint: disable=unused-import
from adafruit_epd.ssd1675 import Adafruit_SSD1675  # pylint: disable=unused-import
from adafruit_epd.ssd1680 import Adafruit_SSD1680  # pylint: disable=unused-import
from adafruit_epd.ssd1681 import Adafruit_SSD1681  # pylint: disable=unused-import
from adafruit_epd.uc8151d import Adafruit_UC8151D  # pylint: disable=unused-import
from adafruit_epd.ek79686 import Adafruit_EK79686  # pylint: disable=unused-import
from adafruit_epd.ssd1680 import Adafruit_SSD1680Z

# First define some color constants
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)

# Next define some constants to allow easy resizing of shapes and colors
BORDER = 20
FONTSIZE = 24
BACKGROUND_COLOR = BLACK
FOREGROUND_COLOR = WHITE
TEXT_COLOR = RED

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
srcs = None
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

# give them all to our driver
# display = Adafruit_SSD1608(200, 200,        # 1.54" HD mono display
# display = Adafruit_SSD1675(122, 250,        # 2.13" HD mono display
#display = Adafruit_SSD1680(122, 250,        # 2.13" HD Tri-color or mono display
# display = Adafruit_SSD1681(200, 200,        # 1.54" HD Tri-color display
# display = Adafruit_IL91874(176, 264,        # 2.7" Tri-color display
# display = Adafruit_EK79686(176, 264,        # 2.7" Tri-color display
# display = Adafruit_IL0373(152, 152,         # 1.54" Tri-color display
# display = Adafruit_UC8151D(128, 296,        # 2.9" mono flexible display
# display = Adafruit_IL0373(128, 296,         # 2.9" Tri-color display
# display = Adafruit_IL0398(400, 300,         # 4.2" Tri-color display
# display = Adafruit_IL0373(104, 212,         # 2.13" Tri-color display
display = Adafruit_SSD1680Z(122, 250,        # 2.13" HD Tri-color or mono display
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy,
)

# IF YOU HAVE A 2.13" FLEXIBLE DISPLAY uncomment these lines!
# display.set_black_buffer(1, False)
# display.set_color_buffer(1, False)

# IF YOU HAVE A 2.9" FLEXIBLE DISPLAY uncomment these lines!
# display.set_black_buffer(1, True)
# display.set_color_buffer(1, True)

display.rotation = 1

# ---

# image = Image.open("blinka.png")

# # Scale the image to the smaller screen dimension
# image_ratio = image.width / image.height
# screen_ratio = display.width / display.height
# if screen_ratio < image_ratio:
#     scaled_width = image.width * display.height // image.height
#     scaled_height = display.height
# else:
#     scaled_width = display.width
#     scaled_height = image.height * display.width // image.width
# image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# # Crop and center the image
# x = scaled_width // 2 - display.width // 2
# y = scaled_height // 2 - display.height // 2
# image = image.crop((x, y, x + display.width, y + display.height)).convert("RGB")

# # Convert to Monochrome and Add dithering
# image = image.convert("1").convert("L")

# # Display image.
# display.image(image)
# display.display()

# ---

image = Image.new("RGB", (display.width, display.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a filled box as the background
draw.rectangle((0, 0, display.width - 1, display.height - 1), fill=BACKGROUND_COLOR)

# Draw a smaller inner foreground rectangle
draw.rectangle(
    (BORDER, BORDER, display.width - BORDER - 1, display.height - BORDER - 1),
    fill=FOREGROUND_COLOR,
)

# Load a TTF Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

# Draw Some Text
text = "Hello World!"
(font_width, font_height) = font.getsize(text)
draw.text(
    (display.width // 2 - font_width // 2, display.height // 2 - font_height // 2),
    text,
    font=font,
    fill=TEXT_COLOR,
)

# Display image.
display.image(image)
display.display()
