import pandas as pd
import pytest
from sklearn.tree import DecisionTreeClassifier

from fraud_detection.models.explainability import (
    extract_feature_importances,
    format_feature_importances,
)


def test_extract_feature_importances_returns_sorted_rows():
    features = pd.DataFrame({"amount": [1, 2, 100, 200], "hour": [1, 1, 1, 1]})
    model = DecisionTreeClassifier(random_state=42).fit(features, [0, 0, 1, 1])

    rows = extract_feature_importances(
        {"model": model, "feature_columns": ["amount", "hour"]}
    )

    assert rows[0]["feature"] == "amount"
    assert rows[0]["importance"] >= rows[1]["importance"]
    assert "Importance" in format_feature_importances(rows)


def test_extract_feature_importances_rejects_unsupported_model():
    with pytest.raises(ValueError, match="feature_importances"):
        extract_feature_importances({"model": object(), "feature_columns": []})
