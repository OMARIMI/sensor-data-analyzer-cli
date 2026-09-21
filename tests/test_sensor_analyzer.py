import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sensor_analyzer


class SensorAnalyzerTests(unittest.TestCase):
    def analyze_csv(self, csv_text, thresholds=None):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "readings.csv"
            output_file = temp_path / "report.json"
            input_file.write_text(csv_text, encoding="utf-8")

            with patch("builtins.print"):
                sensor_analyzer.analyze_file(
                    str(input_file),
                    str(output_file),
                    thresholds,
                )

            return json.loads(output_file.read_text(encoding="utf-8"))

    def test_analyze_sensor_calculates_stats(self):
        result = sensor_analyzer.analyze_sensor([10, 20, 30])

        self.assertEqual(result["count"], 3)
        self.assertEqual(result["min"], 10)
        self.assertEqual(result["max"], 30)
        self.assertEqual(result["average"], 20)

    def test_normal_file_creates_expected_report(self):
        report = self.analyze_csv(
            "timestamp,temperature_c,humidity_percent,vibration_g\n"
            "2026-06-01T10:00:00,22.5,45,0.02\n"
            "2026-06-01T10:01:00,23.5,47,0.04\n"
        )

        self.assertEqual(report["sensors"]["temperature_c"]["count"], 2)
        self.assertEqual(report["sensors"]["temperature_c"]["average"], 23.0)
        self.assertEqual(report["invalid_data"], [])
        self.assertEqual(report["warnings"], [])

    def test_boundary_values_do_not_trigger_warnings(self):
        report = self.analyze_csv(
            "timestamp,temperature_c,humidity_percent,vibration_g\n"
            "2026-06-01T10:00:00,80,90,0.15\n"
        )

        self.assertEqual(report["warnings"], [])

    def test_values_above_threshold_trigger_warnings(self):
        report = self.analyze_csv(
            "timestamp,temperature_c,humidity_percent,vibration_g\n"
            "2026-06-01T10:00:00,80.1,90.1,0.16\n"
        )

        self.assertEqual(len(report["warnings"]), 3)
        self.assertIn("temperature_c is high", report["warnings"][0])

    def test_custom_threshold_changes_warning_behavior(self):
        report = self.analyze_csv(
            "timestamp,temperature_c,humidity_percent,vibration_g\n"
            "2026-06-01T10:00:00,25,45,0.02\n",
            {"temperature_c": 24},
        )

        self.assertEqual(report["thresholds"]["temperature_c"], 24)
        self.assertEqual(len(report["warnings"]), 1)
        self.assertIn("25.0 > 24", report["warnings"][0])

    def test_empty_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "readings.csv"
            output_file = temp_path / "report.json"
            input_file.write_text("", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "empty"):
                sensor_analyzer.analyze_file(str(input_file), str(output_file))

            self.assertFalse(output_file.exists())

    def test_malformed_value_is_reported_without_crashing(self):
        report = self.analyze_csv(
            "timestamp,temperature_c,humidity_percent,vibration_g\n"
            "2026-06-01T10:00:00,bad,45,0.02\n"
        )

        self.assertIsNone(report["sensors"]["temperature_c"])
        self.assertIn(
            "invalid number for temperature_c: bad",
            report["invalid_data"][0],
        )

    def test_wrong_unit_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / "readings.csv"
            output_file = temp_path / "report.json"
            input_file.write_text(
                "timestamp,temperature_f,humidity_percent,vibration_g\n"
                "2026-06-01T10:00:00,72,45,0.02\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "temperature_c"):
                sensor_analyzer.analyze_file(str(input_file), str(output_file))

            self.assertFalse(output_file.exists())

    def test_cli_returns_error_for_bad_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "empty.csv"
            input_file.write_text("", encoding="utf-8")

            with patch("sys.stderr", new_callable=io.StringIO) as error_output:
                exit_code = sensor_analyzer.main([str(input_file)])

            self.assertEqual(exit_code, 1)
            self.assertIn("Error: Input CSV is empty", error_output.getvalue())


if __name__ == "__main__":
    unittest.main()
