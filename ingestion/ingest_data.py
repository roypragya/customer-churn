import pandas as pd

def ingest_csv(path): 
    df = pd.read_csv(path) 
    df.to_csv('data/raw/raw_data.csv', index=False) 
    print("Data ingested successfully.")

if __name__ == "__main__": ingest_csv('data/sample_data.csv')
