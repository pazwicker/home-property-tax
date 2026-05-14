# home-property-tax

HCAD (Harris County Appraisal District) data pipeline and property tax protest analysis. Extracts public data from HCAD and loads it into BigQuery (`zwickfi.hcad`) for analysis.

## Tables

| Table | Description |
|-------|-------------|
| `zwickfi.hcad.real_acct` | Real property account and valuation data (2005–present) |
| `zwickfi.hcad.arb_hearings_real` | Appraisal Review Board hearing records (2005–present) |

## Setup

**Prerequisites:** Python 3.11+, gcloud CLI authenticated to the `zwickfi` project.

```bash
# Authenticate (one-time)
gcloud auth application-default login

# Install dependencies
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Running the pipeline

```bash
# Smart mode — full history on first run, prior + current year on subsequent runs
python run.py

# Load specific years
python run.py --years 2024 2025

# Force reload all history (2005–present)
python run.py --full-refresh
```

The pipeline is idempotent — re-running the same years is safe, existing rows are replaced.

## Analysis

Property tax protest analysis lives in [`wickersham/tax_year_2023/`](wickersham/tax_year_2023/). The Jupyter notebooks there query the BigQuery tables (or the legacy SQLite database) to produce neighborhood comparables, market trend charts, and protest evidence.
