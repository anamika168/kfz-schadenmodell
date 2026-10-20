"""Download the French motor third-party liability data and save it as parquet.

Two tables:
    freMTPL2freq  one row per policy: exposure, declared claim count and risk features
    freMTPL2sev   one row per claim: policy ID and claim amount

Source: the R package CASdatasets (A. Charpentier, C. Dutang), release of January 2017, pinned to
one commit of its GitHub repository. OpenML hosts the same release (data IDs 41214 and 41215,
678,013 policies and 26,639 claims). CASdatasets releases from 2022 onwards removed inconsistencies
that notebook 01 finds, so the analysis is pinned to the 2017 release.

Run from the repository root:  python get_data.py
"""
from pathlib import Path
from urllib.request import urlretrieve

import rdata

COMMIT = "9aa07b9d7f07c6d877674decc95503bf1f0fd8c5"
BASE_URL = f"https://raw.githubusercontent.com/dutangc/CASdatasets/{COMMIT}/pkg/data/"
DATA_DIR = Path(__file__).resolve().parent / "data"


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for name in ["freMTPL2freq", "freMTPL2sev"]:
        rda_file = DATA_DIR / f"{name}.rda"
        if not rda_file.exists():
            urlretrieve(BASE_URL + f"{name}.rda", rda_file)
        frame = rdata.read_rda(rda_file)[name].reset_index(drop=True)
        frame.to_parquet(DATA_DIR / f"{name}.parquet", index=False)
        print(f"{name}: {frame.shape[0]:,} rows, {frame.shape[1]} columns")


if __name__ == "__main__":
    main()
