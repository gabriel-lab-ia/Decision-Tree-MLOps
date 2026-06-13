# Model Explainability

Decision Trees are interpretable because each prediction follows explicit feature
thresholds from the root to a leaf. The v0.2 explainability command exports the model's
global feature importances:

```bash
make train
make explain
```

Feature importance measures how much each feature reduced impurity across the fitted
tree. It helps identify the signals most influential to this fraud baseline and is
useful for debugging, review, and communication.

Global importance does not explain an individual decision, establish causality, prove
fairness, or reveal correlated-feature effects reliably. Production use should add
per-prediction explanations, stability checks, bias analysis, and domain review.
