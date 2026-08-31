"""
api/weather.py
---------------
Same get_weather() logic as your original weather_app.py — the only
difference is it's triggered by an HTTP GET request instead of terminal
input(), and returns an HTML page instead of printing to console.
"""

import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str, api_key: str) -> dict:
    """Identical to weather_app.py — calls OpenWeatherMap and returns JSON."""
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def render_result(data: dict) -> str:
    """Same fields as your display_weather() — built as a styled HTML block."""
    city = data["name"]
    country = data["sys"]["country"]
    temp = round(data["main"]["temp"])
    feels_like = round(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    description = data["weather"][0]["description"].title()
    wind_speed = data["wind"]["speed"]
    pressure = data["main"]["pressure"]

    return f"""
    <div class="reading">
      <div class="location">{city}, {country}</div>
      <div class="temp-row">
        <div class="temp">{temp}&deg;</div>
        <div class="condition">{description}</div>
      </div>
      <div class="feels-like">Feels like {feels_like}&deg;</div>
      <div class="stats">
        <div class="stat">
          <div class="stat-label">Humidity</div>
          <div class="stat-value">{humidity}%</div>
        </div>
        <div class="stat">
          <div class="stat-label">Wind</div>
          <div class="stat-value">{wind_speed} m/s</div>
        </div>
        <div class="stat">
          <div class="stat-label">Pressure</div>
          <div class="stat-value">{pressure} hPa</div>
        </div>
      </div>
    </div>
    """


def render_page(body: str) -> str:
    """Dark, cinematic-styled page shell — matches the portfolio aesthetic."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Weather Readout</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Anton&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #09090B;
                --surface: #131316;
                --line: #232328;
                --gold: #D9A94E;
                --text: #F4F4F2;
                --muted: #8A8A8E;
                --error: #C4483A;
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                background: var(--bg);
                color: var(--text);
                font-family: 'JetBrains Mono', monospace;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 24px;
            }}
            main {{ width: 100%; max-width: 420px; }}
            .label {{ font-size: 12px; color: var(--muted); margin-bottom: 6px; }}
            h1 {{
                font-family: 'Anton', sans-serif;
                font-size: 28px;
                font-weight: 400;
                margin-bottom: 28px;
            }}
            form {{ display: flex; gap: 8px; margin-bottom: 24px; }}
            input {{
                flex: 1;
                background: var(--surface);
                border: 1px solid var(--line);
                color: var(--text);
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                padding: 12px 14px;
                border-radius: 4px;
                outline: none;
            }}
            input:focus {{ border-color: var(--gold); }}
            input::placeholder {{ color: var(--muted); }}
            button {{
                background: var(--gold);
                color: #1a1305;
                border: none;
                font-family: 'JetBrains Mono', monospace;
                font-weight: 700;
                font-size: 14px;
                padding: 0 20px;
                border-radius: 4px;
                cursor: pointer;
            }}
            button:hover {{ opacity: 0.85; }}
            .rule {{ height: 1px; background: var(--line); margin-bottom: 24px; }}
            .empty {{ color: var(--muted); font-size: 14px; line-height: 1.6; }}
            .error {{ color: var(--error); font-size: 14px; line-height: 1.6; }}
            .location {{ font-size: 14px; color: var(--muted); margin-bottom: 4px; }}
            .temp-row {{ display: flex; align-items: baseline; gap: 16px; margin-bottom: 4px; }}
            .temp {{ font-family: 'Anton', sans-serif; font-size: 80px; line-height: 1; }}
            .condition {{ font-size: 16px; color: var(--gold); }}
            .feels-like {{ font-size: 13px; color: var(--muted); margin-bottom: 28px; }}
            .stats {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }}
            .stat {{ border-left: 2px solid var(--line); padding-left: 10px; }}
            .stat-label {{ font-size: 11px; color: var(--muted); margin-bottom: 4px; }}
            .stat-value {{ font-size: 18px; font-weight: 500; }}
            @media (max-width: 480px) {{ .temp {{ font-size: 60px; }} }}
        </style>
    </head>
    <body>
        <main>
            <div class="label">Live conditions</div>
            <h1>Weather Readout</h1>
            <form action="/api/weather" method="get">
                <input type="text" name="city" placeholder="Enter a city, e.g. Kanpur" required />
                <button type="submit">Check</button>
            </form>
            <div class="rule"></div>
            {body}
        </main>
    </body>
    </html>
    """


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        city = query.get("city", [None])[0]

        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not city:
            html = render_page('<div class="empty">Search a city to see current temperature, conditions, humidity, and wind.</div>')
        elif not api_key:
            html = render_page('<div class="error">Server is missing OPENWEATHER_API_KEY. Set it in Vercel Environment Variables.</div>')
        else:
            try:
                data = get_weather(city, api_key)
                html = render_page(render_result(data))
            except requests.exceptions.HTTPError:
                html = render_page(f'<div class="error">Could not find weather data for "{city}". Check the spelling and try again.</div>')
            except requests.exceptions.RequestException:
                html = render_page('<div class="error">Network error reaching the weather service.</div>')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())
        return
