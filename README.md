# Weather App

A simple command-line weather application that fetches real-time weather data
for any city using the OpenWeatherMap REST API.

## Features
- Fetches live temperature, "feels like" temperature, humidity, wind speed,
  and weather condition for any city worldwide
- Clean, readable console output
- Graceful error handling for invalid city names or network issues

## Tech Stack
- Python 3
- `requests` — handles HTTP calls to the OpenWeatherMap REST API

## Setup

```bash
git clone https://github.com/aditiupadhyay17/weather-app.git
cd weather-app
pip install -r requirements.txt
```

### Get an API Key
1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/api)
2. Generate an API key from your account dashboard
3. Set it as an environment variable:

```bash
# Windows (PowerShell)
setx OPENWEATHER_API_KEY "your_key_here"

# Mac/Linux
export OPENWEATHER_API_KEY="your_key_here"
```

## Run

```bash
python weather_app.py
```

Example:
```
Enter city name: Kanpur

Weather in Kanpur, IN
------------------------------
Condition:    Clear Sky
Temperature:  32.1°C (feels like 35.4°C)
Humidity:     48%
Wind Speed:   3.2 m/s
------------------------------
```

## Future Improvements
- Add a GUI using Tkinter or a web front-end
- Add a 5-day forecast view
- Cache recent searches to reduce API calls
