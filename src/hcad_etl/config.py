HCAD_BASE_URL = "https://download.hcad.org/data/CAMA"
FIRST_YEAR = 2005

BQ_PROJECT = "zwickfi"
BQ_DATASET = "hcad"
BQ_LOCATION = "US"

# Maps table name → (zip file stem, tsv file stem)
TABLES = {
    "real_acct": ("Real_acct_owner", "real_acct"),
    "arb_hearings_real": ("Hearing_files", "arb_hearings_real"),
}

# Column used to identify which year a row belongs to, per table
YEAR_COLUMNS = {
    "real_acct": "yr",
    "arb_hearings_real": "Tax_Year",
}
