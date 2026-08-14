from pathlib import Path
import json

REPORT_FILE = Path("data/processed/arrival_forecast_model_report.json")
MODEL_CARD_FILE = Path("docs/model_card.md")


def main() -> None:
    if not REPORT_FILE.exists():
        raise FileNotFoundError(
            "Model report not found. Run: "
            "python src/ml/train_arrival_forecast.py"
        )

    with REPORT_FILE.open(encoding="utf-8") as file:
        report = json.load(file)

    baseline = report["baseline_metrics"]
    machine_learning = report["machine_learning_metrics"]

    preferred_method = (
        "Random forest regression"
        if report["preferred_method"] == "random_forest"
        else "Seasonal naive baseline"
    )

    model_card = f"""# Model Card: Singapore Visitor Arrival Forecasting

## Model summary

This project compares a machine-learning model with a simple seasonal baseline
to forecast monthly international visitor arrivals in Singapore.

The model uses only historical official arrival data and calendar-derived
seasonality features. It is an exploratory portfolio model and is not an
official tourism forecast.

## Intended use

- Demonstrate transparent time-series forecasting using official data.
- Compare a machine-learning method with a simple baseline.
- Support learning about seasonality, backtesting, and model evaluation.

## Out-of-scope use

This model must not be used to:

- make immigration, visa, policing, or enforcement decisions;
- judge visitors, nationalities, countries, or groups;
- infer visitor behaviour, cultural respect, resident wellbeing, or tourism impact;
- establish causal effects of policies, events, or interventions;
- replace official tourism forecasts or planning processes.

## Data

| Field | Value |
|---|---|
| Input dataset | {report["dataset"]} |
| Source | {report["source_agency"]} |
| Table ID | {report["source_table_id"]} |
| Data type | Official aggregate monthly tourism statistics |
| Personal data used | No |
| Social-media data used | No |

## Methods compared

### Baseline

**Method:** {report["baseline_method"]}

This predicts a month using the recorded arrivals from the same month in the
previous year.

### Machine-learning model

**Method:** {report["machine_learning_method"]}

The model uses historical arrivals and the following features:

- one-month lag;
- three-month lag;
- twelve-month lag;
- three-month rolling mean;
- month-of-year seasonality features;
- time trend.

## Evaluation design

| Field | Value |
|---|---|
| Training data ended | {report["training_end_date"]} |
| Held-out test started | {report["test_start_date"]} |
| Held-out test ended | {report["test_end_date"]} |
| Test duration | {report["test_months"]} months |
| Preferred method on this test | {preferred_method} |

The held-out test period was not used to train the model.

## Evaluation results

| Method | MAE | RMSE | WAPE |
|---|---:|---:|---:|
| Same month last year baseline | {baseline["mae"]:,.2f} | {baseline["rmse"]:,.2f} | {baseline["wape_pct"]:.2f}% |
| Random forest regression | {machine_learning["mae"]:,.2f} | {machine_learning["rmse"]:,.2f} | {machine_learning["wape_pct"]:.2f}% |

**Interpretation:** Lower MAE, RMSE, and WAPE indicate lower error. The preferred
method is selected only from this held-out comparison.

## Random-forest feature importance

"""

    for feature, importance in report["feature_importance"].items():
        model_card += f"- `{feature}`: {importance:.4f}\n"

    model_card += """

## Limitations

- The model relies on historical arrival patterns and does not know future
  events, policies, border restrictions, flight capacity, weather, or economic
  changes.
- COVID-era disruption may make normal seasonal patterns less reliable.
- A good backtest does not prove a model will remain accurate in the future.
- The model is not evidence that tourism volume causes any social,
  environmental, cultural, or economic outcome.
- The model has not been designed for high-stakes or automated decision-making.

## Version information

- Model type: Random forest regression compared with seasonal naive baseline
- Random seed: 42
- Project: Visitor Respect & Sustainable Tourism Observatory
"""

    MODEL_CARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    MODEL_CARD_FILE.write_text(model_card, encoding="utf-8")

    print(f"Model card created: {MODEL_CARD_FILE}")


if __name__ == "__main__":
    main()