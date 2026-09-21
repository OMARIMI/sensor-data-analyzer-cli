# Verified Demo

Verified on September 21, 2026.

## Successful Sensor Analysis

Command:

```powershell
python sensor_analyzer.py sample_data/readings.csv --output results/report.json --temperature-threshold 30
```

Observed result:

- Exit code `0`.
- Calculated count, minimum, maximum, and average for all three sensors.
- Reported two deliberately invalid values without crashing.
- Applied the custom `30.0` Celsius temperature threshold.
- Saved the structured JSON report.

## Public HTTP Data

Commands:

```powershell
python weather_data.py
python weather_data.py --live
```

Observed result for both saved and live modes:

```text
HTTP status: 200
```

The program selected and printed the observation time, temperature, relative
humidity, wind speed, and their units. No API key was used.

## Safe Failure

Command:

```powershell
python sensor_analyzer.py sample_data/broken/wrong_unit.csv --output results/should-not-exist.json
```

Observed result:

```text
Error: Missing required sensor columns: temperature_c. Sensor units are encoded in the column names.
```

The command returned exit code `1`, printed no traceback, and did not create an
output report.
