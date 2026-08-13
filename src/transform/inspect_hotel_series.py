from pathlib import Path
import pandas as pd

RAW_FILE = Path("data/raw/m550111_hotel_statistics.csv")
OUTPUT_FILE = Path("data/processed/hotel_series_inventory.csv")

SERIES_COLUMN = "Data Series"


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {RAW_FILE}. Check the filename and location."
        )

    # Load the dataframe without treating the first row as the header yet
    df_raw = pd.read_csv(RAW_FILE, header=None)

    # Dynamically find which row contains our target "Data Series" column header
    header_row_idx = None
    for idx, row in df_raw.iterrows():
        if row.astype(str).str.strip().str.contains(SERIES_COLUMN, case=False).any():
            header_row_idx = idx
            break

    if header_row_idx is None:
        raise ValueError(
            f"Could not find any row containing the header '{SERIES_COLUMN}' in the CSV file."
        )

    # Reload the CSV properly, skipping all unnecessary metadata rows at the top
    df = pd.read_csv(RAW_FILE, skiprows=header_row_idx)
    df.columns = df.columns.str.strip()

    # Double check that the series column is now properly located
    if SERIES_COLUMN not in df.columns:
        raise ValueError(
            f"Expected '{SERIES_COLUMN}' column was not found. "
            f"Found columns: {df.columns.tolist()[:10]}"
        )

    # Filter out empty spacer rows or trailing footnotes (like rows 7-15 in your image)
    df = df[df[SERIES_COLUMN].notna() & (df[SERIES_COLUMN].str.strip() != "")]
    
    # Stop processing when the "Definitions and Footnotes:" section begins
    footnote_idx = df[df[SERIES_COLUMN].str.contains("Definitions and Footnotes|Variables", case=False, na=False)].index
    if not footnote_idx.empty:
        df = df.loc[:footnote_idx[0] - 1]

    inventory = pd.DataFrame(
        {
            "series_number": range(1, len(df) + 1),
            "data_series": df[SERIES_COLUMN].astype(str).str.strip(),
        }
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    inventory.to_csv(OUTPUT_FILE, index=False)

    print("\nHotel data shape:", df.shape)
    print("\nAvailable data series:")
    print(inventory.to_string(index=False))
    print(f"\nSaved inventory to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
