import pandas as pd

def preprocess(): 
    df = pd.read_csv('data/raw/raw_data.csv') 
    df.dropna(inplace=True) 
    df.drop_duplicates(inplace=True) 
    df.to_csv('data/processed/cleaned_data.csv', index=False) 
    print("Data preprocessed.")

if __name__ == "__main__": preprocess()
