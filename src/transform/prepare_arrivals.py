from pathlib import Path
import json
import re

import pandas as pd

RAW_FILE = Path("data/raw/m550001_international_visitor_arrivals.csv")
OUTPUT_FILE = Path("data/processed/singapore_monthly_arrivals.csv")
QUALITY_FILE = Path("data/processed/arrivals_quality_report.json")

SERIES_COLUMN = "Data Series"
TOTAL_SERIES_NAME = "Total International Visitor Arrivals"


def main() -> None:
    # 1. Check the original file exists.
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {RAW_FILE}. Check the filename and location."
        )

    # 2. Read the original SingStat download without changing it.
    raw_df = pd.read_csv(RAW_FILE)
    raw_df.columns = raw_df.columns.str.strip()

    # 3. Check that the expected identifier column exists.
    if SERIES_COLUMN not in raw_df.columns:
        raise ValueError(
            f"Expected column '{SERIES_COLUMN}' was not found. "
            f"Found: {raw_df.columns.tolist()[:10]}"
        )

    # 4. Find the official total-arrivals row using a flexible check.
    total_rows = raw_df[
        raw_df[SERIES_COLUMN]
        .astype(str)
        .str.strip()
        .str.contains(TOTAL_SERIES_NAME, case=False, na=False)
    ]

    if len(total_rows) == 0:
        available_series = raw_df[SERIES_COLUMN].dropna().unique()[:10]
        raise ValueError(
            f"Could not find any row containing '{TOTAL_SERIES_NAME}'.\n"
            f"First 10 available rows in '{SERIES_COLUMN}':\n{available_series}"
        )
    elif len(total_rows) > 1:
        raise ValueError(
            f"Expected exactly one row containing '{TOTAL_SERIES_NAME}', "
            f"but found {len(total_rows)}."
        )

    # 5. Keep only the total-arrivals row, then convert monthly columns to rows.
    total_row = total_rows.copy()

    long_df = total_row.melt(
        id_vars=[SERIES_COLUMN],
        var_name="month_label",
        value_name="arrivals",
    )

    # 6. Keep only labels that look like '2026 Jun'.
    month_pattern = r"^\d{4}\s[A-Za-z]{3}$"
    long_df = long_df[
        long_df["month_label"].astype(str).str.match(month_pattern, na=False)
    ].copy()

    # 7. Convert month and arrival values into clean, analysis-ready fields.
    long_df["date"] = pd.to_datetime(
        long_df["month_label"],
        format="%Y %b",
        errors="coerce",
    )

    long_df["arrivals"] = pd.to_numeric(
        long_df["arrivals"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )

    # 8. Select final columns and order dates from oldest to newest.
    cleaned_df = (
        long_df[["date", "arrivals"]]
        .dropna(subset=["date", "arrivals"])
        .sort_values("date")
        .reset_index(drop=True)
    )

    # 9. Data-quality checks.
    if cleaned_df.empty:
        raise ValueError("No valid monthly arrival records were created.")

    if cleaned_df["date"].duplicated().any():
        raise ValueError("Duplicate monthly dates were found.")

    if (cleaned_df["arrivals"] < 0).any():
        raise ValueError("Negative arrival values were found.")

    # 10. Add transparent derived fields.
    cleaned_df["year"] = cleaned_df["date"].dt.year
    cleaned_df["month"] = cleaned_df["date"].dt.month
    cleaned_df["month_name"] = cleaned_df["date"].dt.strftime("%B")

    cleaned_df["arrivals_yoy_pct"] = (
        cleaned_df["arrivals"].pct_change(periods=12) * 100
    ).round(1)

    # 11. Save the safe, processed file used later by the website.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(OUTPUT_FILE, index=False)

    # 12. Save a small quality report.
    quality_report = {
        "source_table_id": "M550001",
        "source_agency": "Singapore Tourism Board via SingStat",
        "series_used": TOTAL_SERIES_NAME,
        "record_count": int(len(cleaned_df)),
        "start_date": str(cleaned_df["date"].min().date()),
        "end_date": str(cleaned_df["date"].max().date()),
        "latest_arrivals": int(cleaned_df.iloc[-1]["arrivals"]),
        "missing_arrivals": int(cleaned_df["arrivals"].isna().sum()),
        "duplicate_dates": int(cleaned_df["date"].duplicated().sum()),
    }

    with QUALITY_FILE.open("w", encoding="utf-8") as file:
        json.dump(quality_report, file, indent=2)

    print("Processed file created:", OUTPUT_FILE)
    print("Quality report created:", QUALITY_FILE)
    print("\nFirst 5 cleaned rows:")
    print(cleaned_df.head().to_string(index=False))
    print("\nLast 5 cleaned rows:")
    print(cleaned_df.tail().to_string(index=False))
    print("\nQuality report:")
    print(json.dumps(quality_report, indent=2))


if __name__ == "__main__":
    main()
