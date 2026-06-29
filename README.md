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