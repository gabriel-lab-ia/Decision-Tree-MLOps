from fraud_detection.config import get_settings
from fraud_detection.telemetry.monitoring_queries import (
    average_risk_score,
    fraud_rate_summary,
    recent_predictions,
)
from fraud_detection.telemetry.nosql_client import MongoTelemetryClient


def build_monitoring_summary(client: MongoTelemetryClient) -> dict[str, float | int]:
    fraud = fraud_rate_summary(client)
    return {
        "total_predictions": int(fraud["total"]),
        "fraud_predictions": int(fraud["fraud"]),
        "fraud_prediction_rate": float(fraud["fraud_rate"]),
        "average_risk_score": average_risk_score(client),
        "recent_predictions_count": len(recent_predictions(client)),
    }


def main() -> int:
    client = MongoTelemetryClient(get_settings())
    try:
        summary = build_monitoring_summary(client)
    except Exception as exc:
        print(f"Monitoring unavailable (fail-soft): {exc}")
        return 0
    finally:
        client.close()

    for name, value in summary.items():
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
