import pandas as pd
from sklearn.preprocessing import LabelEncoder

def generate_features(df):
    # Encode segment and region 
    df['segment_encoded'] = LabelEncoder().fit_transform(df['segment']) 
    df['region_encoded'] = LabelEncoder().fit_transform(df['region']) 
    df.to_csv('data/processed/feature_data.csv', index=False) 
    print("Features generated.")
    return df

if __name__ == "__main__": 
    raw_csv='data/sample_data.csv'
    raw_df = pd.read_csv(raw_csv)
    generate_features(df=raw_df)
