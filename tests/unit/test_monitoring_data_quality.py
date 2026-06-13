import pandas as pd

from fraud_detection.monitoring.data_quality import (
    count_missing_values,
    detect_invalid_numeric_ranges,
    summarize_transaction_amount,
)
from fraud_detection.monitoring.performance import (
    summarize_predictions,
    summarize_risk_scores,
)


def test_data_quality_detects_missing_values_and_invalid_ranges():
    data = pd.DataFrame(
        {
            "transaction_amount": [100.0, -1.0, None],
            "transaction_hour": [12, 30, 2],
            "merchant_risk_score": [0.2, 1.4, 0.5],
        }
    )

    assert count_missing_values(data)["transaction_amount"] == 1
    invalid = detect_invalid_numeric_ranges(data)
    assert invalid["transaction_amount"] == 1
    assert invalid["transaction_hour"] == 1
    assert invalid["merchant_risk_score"] == 1


def test_distribution_summaries_handle_data_and_empty_inputs():
    amount = summarize_transaction_amount(
        pd.DataFrame({"transaction_amount": [10.0, 20.0, 30.0]})
    )
    assert amount["mean"] == 20.0
    assert summarize_transaction_amount(pd.DataFrame())["count"] == 0
    assert summarize_risk_scores([])["average"] is None
    assert summarize_predictions([])["fraud_rate"] == 0.0


def test_prediction_and_risk_summaries_are_correct():
    assert summarize_predictions([0, 1, 1]) == {
        "total": 3,
        "fraud": 2,
        "legitimate": 1,
        "fraud_rate": 2 / 3,
    }
    assert summarize_risk_scores([0.1, 0.5, 0.9])["average"] == 0.5
