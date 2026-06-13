from fraud_detection.config import get_settings
from fraud_detection.models.explainability import (
    extract_feature_importances,
    format_feature_importances,
)
from fraud_detection.models.predict import load_model_artifact


def main() -> int:
    artifact = load_model_artifact(get_settings().model_path)
    rows = extract_feature_importances(artifact)
    print(f"Model: {artifact['model_name']} ({artifact['model_version']})")
    print(format_feature_importances(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
