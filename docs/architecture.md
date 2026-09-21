# Architecture

Sensor Data Analyzer CLI is a Python command-line tool that reads a CSV file, analyzes sensor values, and saves a JSON report.

## Flow

CSV sensor file -> sensor_analyzer.py -> validation -> stats + warnings -> JSON report

Saved or live Open-Meteo JSON -> weather_data.py -> selected current readings

## Main Parts

- `main()` reads command-line arguments.
- `load_csv()` loads the input CSV into rows.
- `analyze_file()` checks each sensor value, collects valid values, invalid data, and warnings.
- `analyze_sensor()` calculates count, min, max, and average.
- Command-line flags allow each warning threshold to be changed.
- `weather_data.py` reads a saved response by default or fetches live public data with `--live`.
- The final report is saved to the output JSON path.

## Inputs

The input CSV needs these columns:

- `timestamp`
- `temperature_c`
- `humidity_percent`
- `vibration_g`

## Outputs

The program prints a report in the terminal and saves a JSON report with:

- source file
- thresholds used for the run
- stats for each sensor
- invalid data
- warnings
