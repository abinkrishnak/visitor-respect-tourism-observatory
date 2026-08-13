from pathlib import Path
import json
import re

import pandas as pd

RAW_FILE = Path("data/raw/m550111_hotel_statistics.csv")
OUTPUT_FILE = Path("data/processed/singapore_annual_hotel_statistics.csv")
QUALITY_FILE = Path("data/processed/hotel_statistics_quality_report.json")

SERIES_COLUMN = "Data Series"

SERIES_TO_COLUMN = {
    "Number Of Gazetted Hotels (At End Year) (Number)": "gazetted_hotels",
    "Average Occupancy Rate (Per Cent)": "occupancy_rate_pct",
    "Available Room Nights (Number)": "available_room_nights",
    "Average Room Rate (Dollar)": "average_room_rate_sgd",
    "Room Revenue (Thousand Dollars)": "room_revenue_thousand_sgd",
}


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {RAW_FILE}. Check the filename and location."
        )

    # 1. Read raw CSV without headers to dynamically find where the table starts
    df_raw = pd.read_csv(RAW_FILE, header=None)

    header_row_idx = None
    for idx, row in df_raw.iterrows():
        if row.astype(str).str.strip().str.contains(SERIES_COLUMN, case=False).any():
            header_row_idx = idx
            break

    if header_row_idx is None:
        raise ValueError(
            f"Could not find any row containing the header '{SERIES_COLUMN}' in the CSV file."
        )

    # 2. Reload the CSV skipping the leading metadata rows
    raw_df = pd.read_csv(RAW_FILE, skiprows=header_row_idx)
    raw_df.columns = raw_df.columns.astype(str).str.strip()

    if SERIES_COLUMN not in raw_df.columns:
        raise ValueError(f"Expected column '{SERIES_COLUMN}' was not found.")

    raw_df[SERIES_COLUMN] = raw_df[SERIES_COLUMN].astype(str).str.strip()

    # 3. Clean out trailing footnote rows so they don't break validation
    footnote_mask = raw_df[SERIES_COLUMN].str.contains(
        "Definitions and Footnotes|Variables|Notes", case=False, na=False
    )
    if footnote_mask.any():
        footnote_idx = raw_df[footnote_mask].index[0]
        raw_df = raw_df.loc[:footnote_idx - 1]

    # Filter out empty spacer rows
    raw_df = raw_df[raw_df[SERIES_COLUMN].notna() & (raw_df[SERIES_COLUMN] != "")]

    # 4. Check for expected series data mappings
    available_series = set(raw_df[SERIES_COLUMN])
    expected_series = set(SERIES_TO_COLUMN)
    missing_series = expected_series - available_series

    if missing_series:
        raise ValueError(
            "Expected hotel series were missing: "
            f"{sorted(missing_series)}"
        )

    # Convert annual columns such as 2025, 2024, ... into one row per year.
    long_df = raw_df.melt(
        id_vars=[SERIES_COLUMN],
        var_name="year_label",
        value_name="value",
    )

    long_df = long_df[
        long_df["year_label"].astype(str).str.match(r"^\d{4}$", na=False)
    ].copy()

    long_df["year"] = pd.to_numeric(long_df["year_label"], errors="coerce")
    long_df["value"] = pd.to_numeric(
        long_df["value"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )

    long_df["metric"] = long_df[SERIES_COLUMN].map(SERIES_TO_COLUMN)

    cleaned_df = (
        long_df.dropna(subset=["year", "value", "metric"])
        .pivot(index="year", columns="metric", values="value")
        .reset_index()
        .sort_values("year")
        .reset_index(drop=True)
    )

    expected_columns = ["year", *SERIES_TO_COLUMN.values()]
    missing_columns = set(expected_columns) - set(cleaned_df.columns)

    if missing_columns:
        raise ValueError(
            f"Processed dataset is missing columns: {sorted(missing_columns)}"
        )

    cleaned_df = cleaned_df[expected_columns]

    if cleaned_df["year"].duplicated().any():
        raise ValueError("Duplicate years were found.")

    numeric_columns = [column for column in cleaned_df.columns if column != "year"]

    if (cleaned_df[numeric_columns] < 0).any().any():
        raise ValueError("Negative hotel values were found.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(OUTPUT_FILE, index=False)

    latest = cleaned_df.iloc[-1]

    quality_report = {
        "source_table_id": "M550111",
        "source_agency": "Singapore Tourism Board via SingStat",
        "frequency": "Annual",
        "record_count": int(len(cleaned_df)),
        "start_year": int(cleaned_df["year"].min()),
        "end_year": int(cleaned_df["year"].max()),
        "missing_values": int(cleaned_df.isna().sum().sum()),
        "duplicate_years": int(cleaned_df["year"].duplicated().sum()),
        "latest_year": int(latest["year"]),
        "latest_occupancy_rate_pct": float(latest["occupancy_rate_pct"]),
        "latest_average_room_rate_sgd": float(
            latest["average_room_rate_sgd"]
        ),
        "latest_room_revenue_thousand_sgd": float(
            latest["room_revenue_thousand_sgd"]
        ),
        "interpretation_note": (
            "Figures refer to gazetted hotels. Hotel indicators do not measure "
            "resident wellbeing, site-level crowding, visitor behaviour, or "
            "tourism sustainability on their own."
        ),
    }

    with QUALITY_FILE.open("w", encoding="utf-8") as file:
        json.dump(quality_report, file, indent=2)

    print("Processed file created:", OUTPUT_FILE)
    print("Quality report created:", QUALITY_FILE)
    print("\nProcessed annual hotel statistics:")
    print(cleaned_df.tail().to_string(index=False))
    print("\nQuality report:")
    print(json.dumps(quality_report, indent=2))


if __name__ == "__main__":
    main()
