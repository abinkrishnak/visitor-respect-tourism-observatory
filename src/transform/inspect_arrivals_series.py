from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/m550001_international_visitor_arrivals.csv")
OUTPUT_FILE = Path("data/processed/arrivals_series_inventory.csv")

SERIES_COLUMN = "Data Series"


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {RAW_FILE}. Check the filename and location."
        )

    df = pd.read_csv(RAW_FILE)
    df.columns = df.columns.str.strip()

    if SERIES_COLUMN not in df.columns:
        raise ValueError(
            f"Expected '{SERIES_COLUMN}' column was not found."
        )

    inventory = pd.DataFrame(
        {
            "series_number": range(1, len(df) + 1),
            "data_series": df[SERIES_COLUMN].astype(str).str.strip(),
        }
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    inventory.to_csv(OUTPUT_FILE, index=False)

    print(inventory.to_string(index=False))
    print(f"\nSaved series inventory to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()