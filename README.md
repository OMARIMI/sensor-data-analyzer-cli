# Sensor Data Analyzer CLI

A Python command-line tool that reads sensor data from a CSV file, validates the data, calculates basic statistics, detects threshold warnings, and saves a JSON report.

## What It Does

The tool reads sensor readings for:

- `temperature_c`
- `humidity_percent`
- `vibration_g`

It calculates:

- count
- minimum
- maximum
- average

It also detects:

- missing values
- invalid non-numeric values
- values above warning thresholds

## Why It Matters

Real engineering systems often collect messy sensor data. This project shows how to turn raw readings into a useful report while handling bad data safely.

## Run

```powershell
python sensor_analyzer.py sample_data/readings.csv --output results/report.json
```

Thresholds can be changed from the command line:

```powershell
python sensor_analyzer.py sample_data/readings.csv --temperature-threshold 30 --humidity-threshold 85 --vibration-threshold 0.10
```

## Public HTTP Data Example

The project includes a saved response from the public Open-Meteo API for
repeatable use without an API key. Add `--live` to make a real HTTP request.

```powershell
python weather_data.py
python weather_data.py --live
```

## Run Tests

```powershell
python -m unittest discover -s tests
```

The 13-test suite covers normal data, configurable thresholds, exact threshold
boundaries, an empty file, a malformed value, a wrong-unit column, statistics,
saved weather data, and safe CLI errors.

## Input Format

The CSV must use these headers. Units are encoded in the column names, so a
column such as `temperature_f` is rejected instead of being treated as Celsius.

```csv
timestamp,temperature_c,humidity_percent,vibration_g
2026-06-01T10:00:00,22.5,45,0.02
```

## JSON Report Shape

Each sensor contains `count`, `min`, `max`, and `average`, or `null` when no
valid values were available. Validation problems and threshold violations are
kept in separate lists.

```json
{
  "source_file": "sample_data/readings.csv",
  "thresholds": {
    "temperature_c": 80,
    "humidity_percent": 90,
    "vibration_g": 0.15
  },
  "sensors": {
    "temperature_c": {
      "count": 1,
      "min": 22.5,
      "max": 22.5,
      "average": 22.5
    },
    "humidity_percent": {
      "count": 1,
      "min": 45.0,
      "max": 45.0,
      "average": 45.0
    },
    "vibration_g": {
      "count": 1,
      "min": 0.02,
      "max": 0.02,
      "average": 0.02
    }
  },
  "invalid_data": [],
  "warnings": []
}
```

## Example Output

The program prints a sensor report in the terminal and saves a JSON report to:

```text
results/report.json
```

## Project Structure

```text
sensor_analyzer.py
weather_data.py
sample_data/readings.csv
sample_data/open_meteo_response.json
sample_data/broken/
results/report.json
tests/test_sensor_analyzer.py
tests/test_weather_data.py
docs/architecture.md
docs/demo.md
docs/reflection.md
README.md
.gitignore
requirements.txt
```

## Documentation

- `docs/architecture.md` explains how the program is organized.
- `docs/demo.md` records verified success, HTTP, and failure demonstrations.
- `docs/reflection.md` explains what was learned and what could be improved.

## Current Status

Module 2 project checkpoints complete with automated tests and documentation.

Completed:

- reads CSV data
- validates missing and invalid values
- calculates count, min, max, and average
- detects threshold warnings
- accepts configurable thresholds from the command line
- saves a JSON report
- reads saved or live public weather data without an API key
- includes 13 automated tests
- includes architecture, demo, and reflection docs

## Honest Limitations

- Only supports CSV right now.
- JSON input support has not been added yet.
- Sensor names are fixed to the three documented columns.
- The weather example uses fixed New York coordinates.

## Safety and Privacy

- No API key or secret is required or stored.
- The example data is public weather and synthetic sensor data.
- Invalid files return understandable errors without exposing a traceback.

## AI Assistance Disclosure

This project was built with AI assistance. Omar reviewed and ran the code locally.
