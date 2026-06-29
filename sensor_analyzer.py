import argparse
import csv
import json
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
    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def analyze_file(input_file, output_file):
    rows = load_csv(input_file)

    sensor_values = {
        "temperature_c": [],
        "humidity_percent": [],
        "vibration_g": [],
    }

    invalid_rows = []
    warnings = []

    for line_number, row in enumerate(rows, start=2):
        for sensor_name, limit in SENSORS.items():
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

    with open(output_path, "w") as file:
        json.dump(report, file, indent=2)

    print()
    print(f"Saved report to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Analyze sensor data from a CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV sensor file")
    parser.add_argument(
        "--output",
        default="results/report.json",
        help="Path to save the JSON report",
    )

    args = parser.parse_args()
    analyze_file(args.input_file, args.output)


if __name__ == "__main__":
    main()
