from typing import Any

import pandas as pd

NUMERIC_RANGES: dict[str, tuple[float | None, float | None]] = {
    "transaction_amount": (0, None),
    "transaction_hour": (0, 23),
    "customer_age_days": (0, None),
    "num_previous_transactions": (0, None),
    "merchant_risk_score": (0, 1),
    "device_risk_score": (0, 1),
}


def count_missing_values(data: pd.DataFrame) -> dict[str, int]:
    return {column: int(count) for column, count in data.isna().sum().items()}


def detect_invalid_numeric_ranges(data: pd.DataFrame) -> dict[str, int]:
    invalid: dict[str, int] = {}
    for column, (minimum, maximum) in NUMERIC_RANGES.items():
        if column not in data.columns:
            continue
        values = pd.to_numeric(data[column], errors="coerce")
        mask = pd.Series(False, index=data.index)
        if minimum is not None:
            mask |= values < minimum
        if maximum is not None:
            mask |= values > maximum
        invalid[column] = int(mask.sum())
    return invalid


def summarize_transaction_amount(data: pd.DataFrame) -> dict[str, Any]:
    empty_summary = {
        "count": 0,
        "minimum": None,
        "maximum": None,
        "mean": None,
        "median": None,
    }
    if "transaction_amount" not in data.columns:
        return empty_summary

    values = pd.to_numeric(data["transaction_amount"], errors="coerce").dropna()
    if values.empty:
        return empty_summary

    return {
        "count": int(values.count()),
        "minimum": float(values.min()),
        "maximum": float(values.max()),
        "mean": float(values.mean()),
        "median": float(values.median()),
    }
