# Demo Workflow

The v0.2 demo proves that a trained artifact can be loaded by FastAPI, realistic
transactions can be scored, response contracts are enforced, and prediction telemetry
fails softly.

```bash
make train
make api
```

In another terminal:

```bash
make demo
make telemetry-smoke
make monitoring-summary
make explain
```

For the complete local service stack, run `docker compose up --build`. MongoDB is
optional for inference: unavailable telemetry produces a null event ID without
blocking predictions.
