import os
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, api_key: str) -> dict:
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def render_result(data: dict) -> str:
    city = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]

    return f"""
    <div class="result">
        <h2>Weather in {city}, {country}</h2>
        <p><strong>Condition:</strong> {description}</p>
        <p><strong>Temperature:</strong> {temp}&deg;C (feels like {feels_like}&deg;C)</p>
        <p><strong>Humidity:</strong> {humidity}%</p>
        <p><strong>Wind Speed:</strong> {wind_speed} m/s</p>
    </div>
    """


def render_page(body: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Weather App — Aditi Upadhyay</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f5f7fa; color: #1e293b;
                    max-width: 480px; margin: 60px auto; padding: 0 20px; }}
            h1 {{ font-size: 22px; }}
            form {{ display: flex; gap: 8px; margin: 20px 0; }}
            input {{ flex: 1; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 14px; }}
            button {{ padding: 10px 18px; background: #1f3864; color: white; border: none;
                      border-radius: 6px; cursor: pointer; font-weight: 600; }}
            .result {{ background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px 20px; }}
            .result p {{ margin: 6px 0; font-size: 14px; }}
            .error {{ color: #dc2626; font-size: 14px; }}
            footer {{ margin-top: 30px; font-size: 12px; color: #94a3b8; }}
        </style>
    </head>
    <body>
        <h1>Weather App</h1>
        <form action="/api/weather" method="get">
            <input type="text" name="city" placeholder="Enter a city, e.g. Kanpur" required />
            <button type="submit">Check</button>
        </form>
        {body}
        <footer>Python + OpenWeatherMap REST API &middot;
            <a href="https://github.com/aditiupadhyay17/weather-app" target="_blank">Source on GitHub</a>
        </footer>
    </body>
    </html>
    """


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        city = query.get("city", [None])[0]

        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not city:
            html = render_page("")
        elif not api_key:
            html = render_page(
                '<p class="error">Server is missing OPENWEATHER_API_KEY. '
                "Set it in your Vercel project's Environment Variables.</p>"
            )
        else:
            try:
                data = get_weather(city, api_key)
                html = render_page(render_result(data))
            except requests.exceptions.HTTPError:
                html = render_page(
                    f'<p class="error">Could not find weather data for "{city}". '
                    "Check the spelling and try again.</p>"
                )
            except requests.exceptions.RequestException:
                html = render_page('<p class="error">Network error reaching the weather service.</p>')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())
        return
