from pathlib import Path
import json

import pandas as pd

INPUT_FILE = Path("data/annotation/synthetic_practice_annotations.csv")
OUTPUT_FILE = Path("data/processed/synthetic_annotation_quality_report.json")

LABEL_COLUMNS = [
    "crowding_access",
    "visitor_respect_etiquette",
    "environment_cleanliness",
    "cost_displacement",
    "positive_coexistence",
    "unclear_no_theme",
]


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Could not find {INPUT_FILE}.")

    df = pd.read_csv(INPUT_FILE)

    required_columns = {"document_id", "text", "annotation_note", *LABEL_COLUMNS}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if df["document_id"].duplicated().any():
        raise ValueError("Duplicate document IDs were found.")

    if df["text"].isna().any() or (df["text"].str.strip() == "").any():
        raise ValueError("Empty text records were found.")

    for column in LABEL_COLUMNS:
        values = set(df[column].dropna().unique())
        if not values.issubset({0, 1}):
            raise ValueError(
                f"Column '{column}' must contain only 0 or 1. Found: {values}"
            )

    label_count_per_document = df[LABEL_COLUMNS].sum(axis=1)

    if (label_count_per_document == 0).any():
        raise ValueError("Every document needs at least one label.")

    unclear_with_other_label = (
        (df["unclear_no_theme"] == 1)
        & (label_count_per_document > 1)
    )

    if unclear_with_other_label.any():
        raise ValueError(
            "'unclear_no_theme' cannot be combined with another theme."
        )

    label_distribution = {
        column: int(df[column].sum())
        for column in LABEL_COLUMNS
    }

    report = {
        "dataset_type": "Synthetic practice dataset",
        "purpose": (
            "Annotation and validation practice only. "
            "Not real public-platform data and not research evidence."
        ),
        "document_count": int(len(df)),
        "duplicate_document_ids": int(df["document_id"].duplicated().sum()),
        "documents_with_no_labels": int((label_count_per_document == 0).sum()),
        "label_distribution": label_distribution,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("Annotation validation completed successfully.")
    print(f"Quality report created: {OUTPUT_FILE}")
    print("\nLabel distribution:")
    print(pd.Series(label_distribution).to_string())


if __name__ == "__main__":
    main()