from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/m550001_international_visitor_arrivals.csv")

if not RAW_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {RAW_FILE}. "
        "Check that you downloaded and renamed the SingStat CSV correctly."
    )

df = pd.read_csv(RAW_FILE)

print("Shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10).to_string())

print("\nMissing values by column:")
print(df.isna().sum())