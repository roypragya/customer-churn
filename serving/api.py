from fastapi import FastAPI, Request 
import joblib 
import pandas as pd

app = FastAPI() 
model = joblib.load('models/churn_model.pkl')

@app.post("/predict") 
async def predict(request: Request): 
    data = await request.json() 
    df = pd.DataFrame([data]) 
    df['recent_buyer'] = df['recent_buyer'].astype(int) 
    prediction = model.predict(df[['total_spent', 'visits', 'avg_spent_per_visit', 'recent_buyer', 'segment_encoded', 'region_encoded']])[0] 
    return {"churn_prediction": int(prediction)}
