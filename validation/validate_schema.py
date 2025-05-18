import pandas as pd

def validate_schema(): 
    df = pd.read_csv('data/raw/raw_data.csv') 
    expected_columns = ['customer_id', 'last_purchase', 'total_spent', 'visits', 'avg_spent_per_visit', 'recent_buyer', 'segment', 'region', 'churned'] 
    assert all(col in df.columns for col in expected_columns), "Schema validation failed." 
    print("Schema is valid.")

if __name__ == "__main__": validate_schema()
