import pandas as pd 
import joblib 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score

def train(): 
    df = pd.read_csv('data/processed/feature_data.csv') 
    df['recent_buyer'] = df['recent_buyer'].astype(int) 
    X = df[['total_spent', 'visits', 'avg_spent_per_visit', 'recent_buyer', 'segment_encoded', 'region_encoded']] 
    y = df['churned']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, preds):.2f}")
    joblib.dump(model, 'models/churn_model.pkl')


if __name__ == "__main__": train()
