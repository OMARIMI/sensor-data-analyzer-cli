import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import weather_data


class WeatherDataTests(unittest.TestCase):
    def test_saved_response_loads_with_http_status(self):
        status, data = weather_data.load_saved_weather(weather_data.DEFAULT_SAMPLE)

        self.assertEqual(status, 200)
        self.assertEqual(data["timezone"], "America/New_York")

    def test_summary_selects_values_with_units(self):
        _, data = weather_data.load_saved_weather(weather_data.DEFAULT_SAMPLE)

        summary = weather_data.summarize_weather(data)

        self.assertEqual(summary["temperature"], "21.9 °C")
        self.assertEqual(summary["relative_humidity"], "47 %")
        self.assertEqual(summary["wind_speed"], "18.4 km/h")

    def test_missing_weather_fields_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing fields"):
            weather_data.summarize_weather(
                {
                    "current": {"temperature_2m": 20},
                    "current_units": {"temperature_2m": "°C"},
                }
            )

    def test_invalid_saved_json_returns_cli_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            sample = Path(temp_dir) / "invalid.json"
            sample.write_text("not-json", encoding="utf-8")

            with patch("sys.stderr", new_callable=io.StringIO) as error_output:
                exit_code = weather_data.main(["--sample", str(sample)])

            self.assertEqual(exit_code, 1)
            self.assertIn("Error:", error_output.getvalue())


if __name__ == "__main__":
    unittest.main()
