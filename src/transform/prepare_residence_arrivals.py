from pathlib import Path
import json
import re

import pandas as pd

RAW_FILE = Path("data/raw/m550001_international_visitor_arrivals.csv")
OUTPUT_FILE = Path("data/processed/singapore_arrivals_by_residence.csv")
QUALITY_FILE = Path("data/processed/residence_arrivals_quality_report.json")

SERIES_COLUMN = "Data Series"

AGGREGATE_SERIES = {
    "Total International Visitor Arrivals By Place Of Residence",
    "Southeast Asia",
    "Greater China",
    "North Asia",
    "South Asia",
    "West Asia",
    "Europe",
    "North America",
    "Oceania",
    "Africa",
}


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {RAW_FILE}. Check the filename and location."
        )

    raw_df = pd.read_csv(RAW_FILE)
    raw_df.columns = raw_df.columns.str.strip()
    raw_df[SERIES_COLUMN] = raw_df[SERIES_COLUMN].astype(str).str.strip()

    if SERIES_COLUMN not in raw_df.columns:
        raise ValueError(f"Expected '{SERIES_COLUMN}' was not found.")

    # Keep named places only. Remove national total, regional totals,
    # and non-specific 'Other Markets' buckets.
    residence_df = raw_df[
        ~raw_df[SERIES_COLUMN].isin(AGGREGATE_SERIES)
        & ~raw_df[SERIES_COLUMN].str.startswith("Other Markets", na=False)
    ].copy()

    long_df = residence_df.melt(
        id_vars=[SERIES_COLUMN],
        var_name="month_label",
        value_name="arrivals",
    )

    month_pattern = r"^\d{4}\s[A-Za-z]{3}$"
    long_df = long_df[
        long_df["month_label"].astype(str).str.match(month_pattern, na=False)
    ].copy()

    long_df["date"] = pd.to_datetime(
        long_df["month_label"],
        format="%Y %b",
        errors="coerce",
    )

    long_df["arrivals"] = pd.to_numeric(
        long_df["arrivals"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )

    cleaned_df = (
        long_df.rename(columns={SERIES_COLUMN: "place_of_residence"})[
            ["date", "place_of_residence", "arrivals"]
        ]
        .dropna(subset=["date", "place_of_residence", "arrivals"])
        .sort_values(["date", "arrivals"], ascending=[True, False])
        .reset_index(drop=True)
    )

    if cleaned_df.empty:
        raise ValueError("No valid residence-level arrival records were created.")

    if cleaned_df.duplicated(["date", "place_of_residence"]).any():
        raise ValueError(
            "Duplicate date and place-of-residence combinations were found."
        )

    if (cleaned_df["arrivals"] < 0).any():
        raise ValueError("Negative arrival values were found.")

    cleaned_df["year"] = cleaned_df["date"].dt.year
    cleaned_df["month"] = cleaned_df["date"].dt.month
    cleaned_df["month_name"] = cleaned_df["date"].dt.strftime("%B")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(OUTPUT_FILE, index=False)

    latest_date = cleaned_df["date"].max()
    latest_top_10 = cleaned_df[cleaned_df["date"].eq(latest_date)].head(10)

    quality_report = {
        "source_table_id": "M550001",
        "source_agency": "Singapore Tourism Board via SingStat",
        "record_count": int(len(cleaned_df)),
        "named_places_of_residence": int(
            cleaned_df["place_of_residence"].nunique()
        ),
        "start_date": str(cleaned_df["date"].min().date()),
        "end_date": str(latest_date.date()),
        "duplicate_date_place_pairs": int(
            cleaned_df.duplicated(["date", "place_of_residence"]).sum()
        ),
        "missing_arrivals": int(cleaned_df["arrivals"].isna().sum()),
        "exclusions": (
            "National total, regional aggregates, and 'Other Markets' "
            "categories are excluded from this dataset."
        ),
    }

    with QUALITY_FILE.open("w", encoding="utf-8") as file:
        json.dump(quality_report, file, indent=2)

    print("Processed file created:", OUTPUT_FILE)
    print("Quality report created:", QUALITY_FILE)
    print(f"\nTop 10 named places of residence — {latest_date.strftime('%B %Y')}:")
    print(
        latest_top_10[
            ["place_of_residence", "arrivals"]
        ].to_string(index=False)
    )
    print("\nQuality report:")
    print(json.dumps(quality_report, indent=2))


if __name__ == "__main__":
    main()