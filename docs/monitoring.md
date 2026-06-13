# Monitoring

Prediction events capture transaction features, prediction, label, risk score, model
identity, and UTC timestamp. The monitoring summary reports total predictions, fraud
prediction count/rate, average risk score, and recent event count.

Data-quality utilities count missing values, flag invalid numeric ranges, and summarize
transaction amounts. Performance utilities summarize risk scores and predicted-class
distribution. These functions are pure and suitable for scheduled jobs or dashboards.

The current summaries are operational signals, not automated drift detection. A v0.3
iteration could add reference distributions, PSI/KS drift metrics, alert thresholds,
latency/error telemetry, and labeled-outcome performance monitoring.
