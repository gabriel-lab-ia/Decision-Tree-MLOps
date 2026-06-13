from collections.abc import Iterable


def summarize_risk_scores(
    risk_scores: Iterable[float],
) -> dict[str, float | int | None]:
    values = [float(value) for value in risk_scores]
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "average": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "average": sum(values) / len(values),
    }


def summarize_predictions(predictions: Iterable[int]) -> dict[str, float | int]:
    values = [int(value) for value in predictions]
    total = len(values)
    fraud = sum(value == 1 for value in values)
    legitimate = sum(value == 0 for value in values)
    return {
        "total": total,
        "fraud": fraud,
        "legitimate": legitimate,
        "fraud_rate": fraud / total if total else 0.0,
    }
