# ink-display

Python Program for Raspberry Pi Zero & Adafruit Monochrome E-Ink Display

## Features

- Display live weather updates using OpenWeather API
- Show real-time stock market data from Alpha Vantage
- Generate and display WiFi QR codes for quick connection
- Fetch and display upcoming subway train arrival times using MTA API

## Dependencies

Ensure you have the following installed:

- [Adafruit CircuitPython](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
- [requests](https://pypi.org/project/requests/)
- [gtfs-realtime-bindings](https://pypi.org/project/gtfs-realtime-bindings/)
- [protobuf](https://pypi.org/project/protobuf/)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (for managing environment variables)
- [qrcode](https://pypi.org/project/qrcode/) (for generating WiFi QR codes)

## Setup `.env` File

Create a `.env` file in the root directory with the following credentials:

```ini
MTA_BUS_TOKEN=mta-bus-token
OPEN_WEATHER_TOKEN=open-weather-token
WIFI_SSID=wifi-ssid
WIFI_PASSWORD=wifi-password
WIFI_AUTH=wifi-auth
ALPHAVANTAGE_API_KEY=alphavantage-key
```

## How to Run

1. **Clone the repository**:

   ```sh
   git clone https://github.com/your-repo/ink-display.git
   cd ink-display
   ```

2. **Install dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

## Useful Links

- [MTA Bus API](https://bustime.mta.info/wiki/Developers/Index)
- [Open Weather API](https://openweathermap.org/api)
- [Alpha Vantage Stock API](https://www.alphavantage.co/)
- [Adafruit E-Ink Display Guide](https://learn.adafruit.com/adafruit-eink-display-breakouts/)
