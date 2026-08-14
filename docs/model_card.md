# Model Card: Singapore Visitor Arrival Forecasting

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
| Input dataset | Singapore monthly international visitor arrivals |
| Source | Singapore Tourism Board via SingStat |
| Table ID | M550001 |
| Data type | Official aggregate monthly tourism statistics |
| Personal data used | No |
| Social-media data used | No |

## Methods compared

### Baseline

**Method:** Same month in previous year

This predicts a month using the recorded arrivals from the same month in the
previous year.

### Machine-learning model

**Method:** Random forest regression

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
| Training data ended | 2025-12-01 |
| Held-out test started | 2026-01-01 |
| Held-out test ended | 2026-06-01 |
| Test duration | 6 months |
| Preferred method on this test | Seasonal naive baseline |

The held-out test period was not used to train the model.

## Evaluation results

| Method | MAE | RMSE | WAPE |
|---|---:|---:|---:|
| Same month last year baseline | 108,619.83 | 112,666.47 | 7.96% |
| Random forest regression | 114,656.14 | 121,177.59 | 8.40% |

**Interpretation:** Lower MAE, RMSE, and WAPE indicate lower error. The preferred
method is selected only from this held-out comparison.

## Random-forest feature importance

- `lag_1`: 0.7604
- `rolling_mean_3`: 0.1012
- `lag_12`: 0.0985
- `lag_3`: 0.0209
- `trend_index`: 0.0144
- `month_sin`: 0.0037
- `month_cos`: 0.0010


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
