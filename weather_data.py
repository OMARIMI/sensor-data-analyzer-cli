import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_SAMPLE = Path(__file__).parent / "sample_data" / "open_meteo_response.json"


def build_url():
    query = urlencode(
        {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "current": (
                "temperature_2m,relative_humidity_2m,wind_speed_10m"
            ),
            "timezone": "America/New_York",
        }
    )
    return f"{API_URL}?{query}"


def fetch_weather(timeout=10):
    request = Request(
        build_url(),
        headers={"User-Agent": "sensor-data-analyzer-learning-project/1.0"},
    )
    with urlopen(request, timeout=timeout) as response:
        status = response.status
        data = json.load(response)

    if status != 200:
        raise RuntimeError(f"Weather service returned HTTP {status}.")

    return status, data


def load_saved_weather(file_path):
    saved = json.loads(Path(file_path).read_text(encoding="utf-8"))
    return saved["http_status"], saved["response"]


def summarize_weather(data):
    current = data.get("current")
    units = data.get("current_units")
    if not isinstance(current, dict) or not isinstance(units, dict):
        raise ValueError("Weather response is missing current readings or units.")

    fields = ("temperature_2m", "relative_humidity_2m", "wind_speed_10m")
    missing = [field for field in fields if field not in current or field not in units]
    if missing:
        raise ValueError(f"Weather response is missing fields: {', '.join(missing)}")

    return {
        "time": current.get("time"),
        "temperature": f"{current['temperature_2m']} {units['temperature_2m']}",
        "relative_humidity": (
            f"{current['relative_humidity_2m']} {units['relative_humidity_2m']}"
        ),
        "wind_speed": f"{current['wind_speed_10m']} {units['wind_speed_10m']}",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read selected current weather fields from Open-Meteo."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Fetch live data instead of using the saved sample response",
    )
    parser.add_argument(
        "--sample",
        default=str(DEFAULT_SAMPLE),
        help="Path to the saved response used without --live",
    )
    args = parser.parse_args(argv)

    try:
        if args.live:
            status, data = fetch_weather()
            source = "live Open-Meteo API"
        else:
            status, data = load_saved_weather(args.sample)
            source = "saved Open-Meteo response"

        summary = summarize_weather(data)
    except (HTTPError, URLError, OSError, RuntimeError, ValueError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"HTTP status: {status}")
    print(f"Data source: {source}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
