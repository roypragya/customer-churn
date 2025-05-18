Customer Churn Prediction Pipeline

This is an end-to-end AI + DataEngineering project that predicts customer churn.

Features:
    Data ingestion and cleaning
    Schema validation
    Feature Engineering
    Model training
    API-based model serving
    Streamlit dashboard

How to run:
    1. Install dependencies
    
    pip install -r requirements.txt

    2. Run each step in order:

    ingestion/ingest_data.py
    validation/validate_schema.py
    pipelines/preprocess.py
    features/feature_engineering.py
    models/train_model.py

    3. Launch API:

    uvicorn serving.api:app --reload

    4. Launch Dashboard

    streamlit run dashboard/app.py
    