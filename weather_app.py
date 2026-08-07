"""
Weather App
------------
A simple command-line weather application that fetches real-time weather
data for any city using the OpenWeatherMap REST API.

Run: python weather_app.py
"""

import os
import sys

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_api_key() -> str:
    """Read the API key from an environment variable."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Error: OPENWEATHER_API_KEY environment variable is not set.")
        print("Get a free key at https://openweathermap.org/api and set it:")
        print("  Windows (PowerShell): setx OPENWEATHER_API_KEY \"your_key\"")
        print("  Mac/Linux: export OPENWEATHER_API_KEY=\"your_key\"")
        sys.exit(1)
    return api_key


def get_weather(city: str, api_key: str) -> dict:
    """Call the OpenWeatherMap API and return the JSON response."""
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def display_weather(data: dict) -> None:
    """Print a clean summary of the weather data."""
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]

    print(f"\nWeather in {city}, {country}")
    print("-" * 30)
    print(f"Condition:    {description}")
    print(f"Temperature:  {temp}°C (feels like {feels_like}°C)")
    print(f"Humidity:     {humidity}%")
    print(f"Wind Speed:   {wind_speed} m/s")
    print("-" * 30)


def main() -> None:
    api_key = get_api_key()
    print("=== Weather App ===")
    city = input("Enter city name: ").strip()

    if not city:
        print("City name cannot be empty.")
        return

    try:
        data = get_weather(city, api_key)
        display_weather(data)
    except requests.exceptions.HTTPError:
        print(f"Could not find weather data for '{city}'. Check the spelling and try again.")
    except requests.exceptions.RequestException as exc:
        print(f"Network error: {exc}")


if __name__ == "__main__":
    main()
