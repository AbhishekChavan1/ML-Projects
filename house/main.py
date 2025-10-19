from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import uvicorn
from model import HousePricePredictor
import numpy as np

app = FastAPI(
    title="House Price Prediction API",
    description="Predict house prices using California Housing Dataset",
    version="1.0.0"
)

predictor = HousePricePredictor()
app.mount("/static", StaticFiles(directory="static"), name="static")


class HouseFeatures(BaseModel):
    MedInc: float = Field(..., description="Median income in block group", ge=0, le=15)
    HouseAge: float = Field(..., description="Median house age in block group", ge=0, le=100)
    AveRooms: float = Field(..., description="Average number of rooms per household", ge=1, le=20)
    AveBedrms: float = Field(..., description="Average number of bedrooms per household", ge=0, le=10)
    Population: float = Field(..., description="Block group population", ge=0, le=10000)
    AveOccup: float = Field(..., description="Average number of household members", ge=0, le=20)
    Latitude: float = Field(..., description="Block group latitude", ge=32, le=42)
    Longitude: float = Field(..., description="Block group longitude", ge=-125, le=-114)

    class Config:
        json_schema_extra = {
            "example": {
                "MedInc": 3.5,
                "HouseAge": 25.0,
                "AveRooms": 5.5,
                "AveBedrms": 1.2,
                "Population": 1500.0,
                "AveOccup": 3.0,
                "Latitude": 37.5,
                "Longitude": -122.0
            }
        }


class PredictionResponse(BaseModel):
    predicted_price: float
    price_in_thousands: float
    features_used: Dict[str, float]


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")


@app.post("/predict", response_model=PredictionResponse)
async def predict_price(features: HouseFeatures):
    try:
        # Convert features to numpy array
        feature_array = np.array([[
            features.MedInc,
            features.HouseAge,
            features.AveRooms,
            features.AveBedrms,
            features.Population,
            features.AveOccup,
            features.Latitude,
            features.Longitude
        ]])
        
        prediction = predictor.predict(feature_array)        
        return PredictionResponse(
            predicted_price=float(prediction[0]),
            price_in_thousands=float(prediction[0] * 100),  # Convert to thousands
            features_used=features.dict()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/dataset-info")
async def get_dataset_info():
    return {
        "dataset_name": "California Housing Dataset",
        "n_samples": predictor.X_train.shape[0] + predictor.X_test.shape[0],
        "n_features": predictor.X_train.shape[1],
        "feature_names": [
            "MedInc", "HouseAge", "AveRooms", "AveBedrms",
            "Population", "AveOccup", "Latitude", "Longitude"
        ],
        "target": "Median house value (in $100,000s)",
        "description": "California housing dataset from the 1990 census"
    }


@app.get("/model-info")
async def get_model_info():
    return predictor.get_model_info()


@app.get("/sample-data")
async def get_sample_data():
    return predictor.get_sample_data(n_samples=5)


@app.post("/retrain")
async def retrain_model():
    try:
        metrics = predictor.train()
        return {
            "status": "success",
            "message": "Model retrained successfully",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@app.get("/feature-importance")
async def get_feature_importance():
    try:
        importance = predictor.get_feature_importance()
        return importance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting feature importance: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
