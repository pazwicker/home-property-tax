"""HCAD → BigQuery pipeline orchestration."""

import argparse
import tempfile
from datetime import datetime
from pathlib import Path

from google.cloud import bigquery

from .config import FIRST_YEAR, TABLES
from .extract import download_and_extract
from .load import delete_year, ensure_dataset_exists, get_client, load_dataframe, table_exists
from .transform import apply_schema


def get_years_to_load(client: bigquery.Client, full_refresh: bool) -> list[int]:
    current_year = datetime.now().year
    if full_refresh:
        return list(range(FIRST_YEAR, current_year + 1))

    if not table_exists(client, "real_acct"):
        print("No existing data found — running full history load.")
        return list(range(FIRST_YEAR, current_year + 1))

    rows = client.query(
        "SELECT MAX(CAST(yr AS INT64)) FROM `zwickfi.hcad.real_acct`"
    ).result()
    max_year = list(rows)[0][0]

    if max_year is None:
        print("Table exists but is empty — running full history load.")
        return list(range(FIRST_YEAR, current_year + 1))

    print(f"Existing data found through {max_year}. Loading incremental years.")
    return [current_year - 1, current_year]


def run_pipeline(years: list[int] | None = None, full_refresh: bool = False) -> None:
    client = get_client()
    ensure_dataset_exists(client)

    if years is not None:
        years_to_load = years
        print(f"Loading specified years: {years_to_load}")
    else:
        years_to_load = get_years_to_load(client, full_refresh)
        print(f"Years to load: {years_to_load[0]}–{years_to_load[-1]} ({len(years_to_load)} years)")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for year in years_to_load:
            for table_name, (zip_stem, tsv_stem) in TABLES.items():
                print(f"\n[{year}] {table_name}")
                try:
                    df = download_and_extract(year, zip_stem, tsv_stem, tmp_dir)
                    df = apply_schema(df, table_name)

                    if table_exists(client, table_name):
                        delete_year(client, table_name, year)

                    rows = load_dataframe(client, df, table_name)
                    print(f"  Loaded {rows:,} rows → zwickfi.hcad.{table_name}")
                except Exception as exc:
                    print(f"  ERROR: {exc}")
                    print(f"  Skipping {table_name} for {year}.")

    print("\nDone.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract HCAD data and load into BigQuery (zwickfi.hcad)."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--full-refresh",
        action="store_true",
        help=f"Load all years from {FIRST_YEAR} to present, replacing existing data.",
    )
    group.add_argument(
        "--years",
        nargs="+",
        type=int,
        metavar="YEAR",
        help="Specific years to load (e.g. --years 2024 2025).",
    )
    args = parser.parse_args()

    run_pipeline(years=args.years, full_refresh=args.full_refresh)


if __name__ == "__main__":
    main()
