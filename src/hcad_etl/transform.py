import pandas as pd


def apply_schema_real_acct(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["acct"] = df["acct"].astype(str)
    df["yr"] = df["yr"].astype(str)
    for col in ("certified_date", "notice_dt", "rev_dt", "new_own_dt", "splt_dt"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def apply_schema_arb_hearings_real(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["acct"] = df["acct"].astype(str)
    df["Tax_Year"] = df["Tax_Year"].astype(str)
    for col in ("Scheduled_for_Date", "Actual_Hearing_Date", "Release_Date"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


SCHEMA_FUNCTIONS = {
    "real_acct": apply_schema_real_acct,
    "arb_hearings_real": apply_schema_arb_hearings_real,
}


def apply_schema(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    fn = SCHEMA_FUNCTIONS.get(table_name)
    if fn is None:
        raise ValueError(f"No schema function defined for table: {table_name}")
    return fn(df)
