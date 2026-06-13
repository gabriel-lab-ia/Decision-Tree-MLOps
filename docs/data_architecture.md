# Data Architecture

This project uses a layered data architecture to keep machine learning training code separated from data access, data cleaning, preprocessing, and feature engineering responsibilities.

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

Layers
Raw Transaction Data

The raw dataset contains transaction-level fraud detection signals such as transaction amount, transaction hour, customer age, transaction history, merchant risk score, device risk score, and the fraud target label.

TransactionDataRepository

TransactionDataRepository acts as a DAO-style boundary for data access. It is responsible for loading raw data, generating the synthetic baseline dataset when needed, saving processed datasets, loading processed datasets, and validating raw transaction data through a dedicated interface.

This keeps training code from being directly coupled to file paths, CSV loading, or persistence details.

Data Cleaning

The cleaning layer handles data quality issues before model training. It removes duplicate rows, coerces numeric columns, handles missing values, removes invalid ranges, and ensures that downstream preprocessing receives stable tabular data.

Examples of invalid ranges include negative transaction amounts, invalid transaction hours, negative customer age, negative transaction history, and risk scores outside the 0 to 1 interval.

Schema Validation

Validation checks whether the cleaned dataset contains the required training columns, valid target labels, and no unacceptable missing values. This protects the model pipeline from silently training on malformed data.

Feature Engineering

Feature engineering transforms raw transaction fields into fraud-oriented model signals, including night transaction flags, new customer flags, low transaction history indicators, high amount transaction indicators, and combined merchant/device risk scores.

Processed Dataset

After cleaning, validation, and feature engineering, the processed dataset is saved as a reproducible local artifact. This gives the training pipeline a clear separation between raw data and model-ready data.

Decision Tree Training

The training layer consumes the processed dataset, splits features and target, trains the DecisionTreeClassifier, evaluates model metrics, logs the experiment to MLflow, and saves the trained model artifact.

Design Benefits
Separates data access from model training
Makes preprocessing testable
Reduces coupling between training and storage
Improves reproducibility
Prepares the project for future production data sources
Makes the ML lifecycle easier to monitor, validate, and extend
Current Implementation
src/fraud_detection/data/
├── cleaning.py
├── pipeline.py
├── preprocessing.py
├── repository.py
├── schemas.py
└── validation.py

Test Coverage

The data architecture is covered by unit tests for:

Data cleaning
DAO/repository behavior
End-to-end training dataset pipeline
tests/unit/
├── test_data_cleaning.py
├── test_data_pipeline.py
└── test_transaction_data_repository.py