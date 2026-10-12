# MP1 Data Pipeline

This command-line pipeline loads a CSV file, validates it, cleans it, and saves the result as a new CSV file. Data flows through four stages in order: loading, validation, processing, and output. `pipeline.py` coordinates the workflow and handles command-line arguments, while all reusable code lives in the `src/` package. `data_loaders.py` reads CSV, JSON, and YAML files, `data_validator.py` checks required columns and removes rows with non-numeric values, `data_processor.py` removes duplicates, missing values, and outliers and builds a cleaning report, and `data_output.py` writes the final CSV. `utils.py` provides shared helpers for logging setup and input-file validation. Every column name and cleaning option is controlled by `config/config.yaml`, so the same code can clean other compatible CSV files without being changed.

## Project structure

```text
mp1-data-pipeline/
├── pipeline.py
├── requirements.txt
├── config/config.yaml
├── src/            (data_loaders, data_validator, data_processor, data_output, utils)
├── fixtures/       (small sample files for testing)
└── output/         (generated results, not committed)
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
21:23:31 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
21:23:31 INFO     src.utils — Input file validated: fixtures/sample_data.csv
21:23:31 INFO     src.utils — Input file validated: config/config.yaml
21:23:31 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
21:23:31 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
21:23:31 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
21:23:31 DEBUG    src.data_validator — Validation: 100 → 98 rows (2 removed)
21:23:31 INFO     __main__ — Validation complete: 100 → 98 rows
21:23:31 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
21:23:31 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
21:23:31 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
21:23:31 INFO     __main__ — Processing complete: 98 → 92 rows
21:23:32 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
21:23:32 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{
    'rows_before': 98,
    'rows_after': 92,
    'rows_removed': 6,
    'columns_before': 5,
    'columns_after': 5,
    'columns_removed': 0,
}
```