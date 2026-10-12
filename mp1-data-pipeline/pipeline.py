
import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Data processing pipeline: load, validate, clean, and save data."
    )
    parser.add_argument(
        "--input", "-i", required=True, help="Path to the input file"
    )
    parser.add_argument(
        "--config", "-c", required=True, help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--output", "-o", required=True, help="Path to the output file"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        "Arguments parsed: input=%s, config=%s, output=%s",
        args.input,
        args.config,
        args.output,
    )

    # Validate files, then load input data and configuration
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # Validate the data
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    rows_loaded = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info("Validation complete: %d → %d rows", rows_loaded, len(data))

    # Process the data
    df_original = data.copy()
    try:
        df_clean = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df_clean)
    logger.info(
        "Processing complete: %d → %d rows", report["rows_before"], report["rows_after"]
    )

    # Save the output
    output_path = save_data(df_clean, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    # Print the cleaning report
    print("\nCleaning report:")
    print("{")
    for key, value in report.items():
        print(f"    '{key}': {value},")
    print("}")


if __name__ == "__main__":
    main()