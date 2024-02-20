# main.py
import pandas as pd
from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel


app = FastAPI()

class PredictionInput(BaseModel):
    Open: float
    High: float
    Low: float
    Close: float
    Adj_Close: float

model_path = "./models/model.joblib"
model = load(model_path)

@app.get("/")
def home():
    return "Model Prediction Zomato stocks"

@app.post("/predict")
def predict(input_data: PredictionInput):
    features = {
            'Open': input_data.Open,
            'High': input_data.High,
            'Low': input_data.Low,
            'Close': input_data.Close,
            'Adj_Close': input_data.Adj_Close
}
    features = pd.DataFrame(features, index=[0])
    prediction = model.predict(features)[0].item()

    return {"prediction": prediction}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

