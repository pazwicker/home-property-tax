import io
import zipfile
from pathlib import Path

import pandas as pd
import requests

from .config import HCAD_BASE_URL


def download_and_extract(year: int, zip_stem: str, tsv_stem: str, tmp_dir: Path) -> pd.DataFrame:
    """Download a single year's zip from HCAD and return the TSV as a DataFrame."""
    url = f"{HCAD_BASE_URL}/{year}/{zip_stem}.zip"
    print(f"  Downloading {url}")
    response = requests.get(url, stream=True, timeout=300)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        # Find the target file — HCAD sometimes includes extra files in the zip
        target = next(
            (name for name in zf.namelist() if Path(name).stem.lower() == tsv_stem.lower()),
            None,
        )
        if target is None:
            available = zf.namelist()
            raise FileNotFoundError(
                f"Could not find {tsv_stem}.txt in {zip_stem}.zip for {year}. "
                f"Available files: {available}"
            )
        extract_path = tmp_dir / f"{tsv_stem}_{year}.txt"
        extract_path.write_bytes(zf.read(target))

    df = pd.read_csv(
        extract_path,
        sep="\t",
        encoding="latin1",
        low_memory=False,
        on_bad_lines="skip",
    )
    extract_path.unlink()
    return df
