# Reflection

In this project, I built a Python CLI that analyzes sensor data from a CSV file.

I learned how to:

- read CSV files with `csv.DictReader`
- use command-line arguments with `argparse`
- validate missing and invalid values
- calculate count, min, max, and average
- detect threshold warnings
- save structured JSON reports
- add basic automated tests with `unittest`

The hardest part was understanding how to separate invalid data from warning data. Invalid data means the value is missing or not a number. Warning data means the value is valid, but outside the safe threshold.

This project matters because real engineering systems use sensor data, and real data is often messy. The program has to handle bad data without crashing.

Future improvements:

- support JSON input
- let users choose custom thresholds
- save cleaner summary reports
- add more tests
- support more sensor columns