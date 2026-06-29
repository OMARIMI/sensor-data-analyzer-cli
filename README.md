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

## Run Tests

```powershell
python -m unittest discover -s tests
```

## Example Output

The program prints a sensor report in the terminal and saves a JSON report to:

```text
results/report.json
```

## Project Structure

```text
sensor_analyzer.py
sample_data/readings.csv
results/report.json
tests/test_sensor_analyzer.py
docs/architecture.md
docs/reflection.md
README.md
.gitignore
requirements.txt
```

## Documentation

- `docs/architecture.md` explains how the program is organized.
- `docs/reflection.md` explains what was learned and what could be improved.

## Current Status

Working CLI prototype with automated tests and documentation.

Completed:

- reads CSV data
- validates missing and invalid values
- calculates count, min, max, and average
- detects threshold warnings
- saves a JSON report
- includes automated tests
- includes architecture and reflection docs

## Honest Limitations

- Only supports CSV right now.
- Sensor names and thresholds are hardcoded.
- JSON input support has not been added yet.
- Custom threshold settings have not been added yet.

## AI Assistance Disclosure

This project was built with AI assistance. Omar reviewed and ran the code locally.
