import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sensor_analyzer


class SensorAnalyzerTests(unittest.TestCase):
    def test_analyze_sensor_calculates_stats(self):
        values = [10, 20, 30]

        result = sensor_analyzer.analyze_sensor(values)

        self.assertEqual(result["count"], 3)
        self.assertEqual(result["min"], 10)
        self.assertEqual(result["max"], 30)
        self.assertEqual(result["average"], 20)

    def test_analyze_file_creates_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "readings.csv"
            output_file = temp_path / "report.json"

            input_file.write_text(
                "timestamp,temperature_c,humidity_percent,vibration_g\n"
                "2026-06-01T10:00:00,22.5,45,0.02\n"
                "2026-06-01T10:01:00,,46,0.03\n"
                "2026-06-01T10:02:00,85.2,bad,0.20\n",
                encoding="utf-8",
            )

            with patch("builtins.print"):
                sensor_analyzer.analyze_file(str(input_file), str(output_file))

            self.assertTrue(output_file.exists())

            report = json.loads(output_file.read_text(encoding="utf-8"))

            self.assertEqual(report["sensors"]["temperature_c"]["count"], 2)
            self.assertEqual(report["sensors"]["temperature_c"]["max"], 85.2)
            self.assertIn("missing value for temperature_c", report["invalid_data"][0])
            self.assertIn("invalid number for humidity_percent", report["invalid_data"][1])
            self.assertEqual(len(report["warnings"]), 2)


if __name__ == "__main__":
    unittest.main()
