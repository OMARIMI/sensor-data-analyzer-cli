import argparse
import csv
import json
import sys
from pathlib import Path

SENSORS = {
    "temperature_c": 80,
    "humidity_percent": 90,
    "vibration_g": 0.15,
}


def analyze_sensor(values):
    count = len(values)

    return {
        "count": count,
        "min": min(values),
        "max": max(values),
        "average": round(sum(values) / count, 2),
    }


def load_csv(file_path):
    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("Input CSV is empty or missing a header row.")

        required_columns = ["timestamp", *SENSORS]
        missing_columns = [
            name for name in required_columns if name not in reader.fieldnames
        ]
        if missing_columns:
            missing = ", ".join(missing_columns)
            raise ValueError(
                f"Missing required sensor columns: {missing}. "
                "Sensor units are encoded in the column names."
            )

        rows = list(reader)
        if not rows:
            raise ValueError("Input CSV contains no sensor readings.")

        return rows


def analyze_file(input_file, output_file, thresholds=None):
    rows = load_csv(input_file)
    active_thresholds = {**SENSORS, **(thresholds or {})}

    sensor_values = {
        "temperature_c": [],
        "humidity_percent": [],
        "vibration_g": [],
    }

    invalid_rows = []
    warnings = []

    for line_number, row in enumerate(rows, start=2):
        for sensor_name, limit in active_thresholds.items():
            raw_value = row.get(sensor_name, "")

            if raw_value == "":
                invalid_rows.append(
                    f"Line {line_number}: missing value for {sensor_name}"
                )
                continue

            try:
                value = float(raw_value)
                sensor_values[sensor_name].append(value)

                if value > limit:
                    warnings.append(
                        f"Line {line_number}: {sensor_name} is high: {value} > {limit}"
                    )

            except ValueError:
                invalid_rows.append(
                    f"Line {line_number}: invalid number for {sensor_name}: {raw_value}"
                )

    report = {
        "source_file": input_file,
        "thresholds": active_thresholds,
        "sensors": {},
        "invalid_data": invalid_rows,
        "warnings": warnings,
    }

    print("SENSOR REPORT")
    print("-------------")

    for sensor_name, values in sensor_values.items():
        print()
        print(sensor_name)

        if values:
            stats = analyze_sensor(values)
            report["sensors"][sensor_name] = stats

            print("Count:", stats["count"])
            print("Min:", stats["min"])
            print("Max:", stats["max"])
            print("Average:", stats["average"])
        else:
            report["sensors"][sensor_name] = None
            print("No valid values found.")

    print()
    print("INVALID DATA")
    print("------------")
    if invalid_rows:
        for problem in invalid_rows:
            print(problem)
    else:
        print("No invalid data found.")

    print()
    print("WARNINGS")
    print("--------")
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No warnings found.")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print()
    print(f"Saved report to {output_file}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analyze sensor data from a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV sensor file")
    parser.add_argument(
        "--output",
        default="results/report.json",
        help="Path to save the JSON report",
    )
    parser.add_argument(
        "--temperature-threshold",
        type=float,
        default=SENSORS["temperature_c"],
        help="Warning threshold in degrees Celsius (default: 80)",
    )
    parser.add_argument(
        "--humidity-threshold",
        type=float,
        default=SENSORS["humidity_percent"],
        help="Warning threshold as a percentage (default: 90)",
    )
    parser.add_argument(
        "--vibration-threshold",
        type=float,
        default=SENSORS["vibration_g"],
        help="Warning threshold in g (default: 0.15)",
    )

    args = parser.parse_args(argv)
    thresholds = {
        "temperature_c": args.temperature_threshold,
        "humidity_percent": args.humidity_threshold,
        "vibration_g": args.vibration_threshold,
    }

    try:
        analyze_file(args.input_file, args.output, thresholds)
    except (FileNotFoundError, PermissionError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
