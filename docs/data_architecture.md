# Data Architecture
This project uses a layered data architecture to keep machine learning training code separated from data access, data cleaning, preprocessing, validation, feature engineering, and model training responsibilities.

## Data Flow

```text
Raw Transaction Data
        ↓
TransactionDataRepository
        ↓
Data Cleaning
        ↓
Schema Validation
        ↓
Feature Engineering
        ↓
Processed Dataset
        ↓
Decision Tree Training
        ↓
MLflow Tracking + Model Artifact
```

## Layers

### Raw Transaction Data

The raw dataset contains transaction-level fraud detection signals such as transaction amount, transaction hour, customer age, transaction history, merchant risk score, device risk score, and the fraud target label.

### TransactionDataRepository

`TransactionDataRepository` acts as a DAO-style boundary for data access.

It is responsible for:

* Loading raw data
* Generating the synthetic baseline dataset when needed
* Saving processed datasets
* Loading processed datasets
* Validating raw transaction data through a dedicated interface

This keeps training code from being directly coupled to file paths, CSV loading, or persistence details.

### Data Cleaning

The cleaning layer handles data quality issues before model training.

It is responsible for:

* Removing duplicate rows
* Coercing numeric columns
* Handling missing values
* Removing invalid ranges
* Producing stable tabular data for downstream preprocessing

Examples of invalid ranges include:

* Negative transaction amounts
* Invalid transaction hours
* Negative customer age
* Negative transaction history
* Risk scores outside the `0` to `1` interval

### Schema Validation

Validation checks whether the cleaned dataset contains the required training columns, valid target labels, and no unacceptable missing values.

This protects the model pipeline from silently training on malformed data.

### Feature Engineering

Feature engineering transforms raw transaction fields into fraud-oriented model signals.

Current engineered features include:

* Night transaction flag
* New customer flag
* Low transaction history indicator
* High amount transaction indicator
* Combined merchant/device risk score

### Processed Dataset

After cleaning, validation, and feature engineering, the processed dataset is saved as a reproducible local artifact.

This gives the training pipeline a clear separation between raw data and model-ready data.

### Decision Tree Training

The training layer consumes the processed dataset, splits features and target, trains the `DecisionTreeClassifier`, evaluates model metrics, logs the experiment to MLflow, and saves the trained model artifact.

## Design Benefits

* Separates data access from model training
* Makes preprocessing testable
* Reduces coupling between training and storage
* Improves reproducibility
* Prepares the project for future production data sources
* Makes the ML lifecycle easier to monitor, validate, and extend

## Current Implementation

```text
src/fraud_detection/data/
├── cleaning.py
├── pipeline.py
├── preprocessing.py
├── repository.py
├── schemas.py
└── validation.py
```

## Test Coverage

The data architecture is covered by unit tests for:

* Data cleaning
* DAO/repository behavior
* End-to-end training dataset pipeline

```text
tests/unit/
├── test_data_cleaning.py
├── test_data_pipeline.py
└── test_transaction_data_repository.py
```
