import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os


class HousePricePredictor:
    def __init__(self, model_path='house_price_model.pkl', scaler_path='scaler.pkl'):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None

        self.load_data()
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.load_model()
        else:
            self.train()
    
    def load_data(self):
        print("Loading California Housing dataset...")
        housing = fetch_california_housing()
        self.X = housing.data
        self.y = housing.target
        self.feature_names = housing.feature_names
        self.target_name = "MedHouseVal"
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )        
        print(f"Dataset loaded: {self.X.shape[0]} samples, {self.X.shape[1]} features")
    
    def train(self):
        print("Training model...")       
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)                
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )        
        self.model.fit(self.X_train_scaled, self.y_train)                
        train_pred = self.model.predict(self.X_train_scaled)
        test_pred = self.model.predict(self.X_test_scaled)
        
        train_rmse = np.sqrt(mean_squared_error(self.y_train, train_pred))
        test_rmse = np.sqrt(mean_squared_error(self.y_test, test_pred))
        train_r2 = r2_score(self.y_train, train_pred)
        test_r2 = r2_score(self.y_test, test_pred)
        train_mae = mean_absolute_error(self.y_train, train_pred)
        test_mae = mean_absolute_error(self.y_test, test_pred)
        
        metrics = {
            "train_rmse": float(train_rmse),
            "test_rmse": float(test_rmse),
            "train_r2": float(train_r2),
            "test_r2": float(test_r2),
            "train_mae": float(train_mae),
            "test_mae": float(test_mae)
        }
        
        print(f"Training completed!")
        print(f"Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
        print(f"Train R²: {train_r2:.4f}, Test R²: {test_r2:.4f}")
        print(f"Train MAE: {train_mae:.4f}, Test MAE: {test_mae:.4f}")
        self.save_model()       
        return metrics
    
    def predict(self, X):
        if self.model is None:
            raise ValueError("Model not trained yet!")       
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        return predictions
    
    def save_model(self):
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        print(f"Model loaded from {self.model_path}")
    
    def get_model_info(self):
        if self.model is None:
            return {"error": "Model not trained yet"}
                
        X_train_scaled = self.scaler.transform(self.X_train)
        X_test_scaled = self.scaler.transform(self.X_test)        
        train_pred = self.model.predict(X_train_scaled)
        test_pred = self.model.predict(X_test_scaled)
        
        return {
            "model_type": "Random Forest Regressor",
            "n_estimators": self.model.n_estimators,
            "max_depth": self.model.max_depth,
            "training_samples": self.X_train.shape[0],
            "test_samples": self.X_test.shape[0],
            "features": self.feature_names,
            "metrics": {
                "train_r2": float(r2_score(self.y_train, train_pred)),
                "test_r2": float(r2_score(self.y_test, test_pred)),
                "train_rmse": float(np.sqrt(mean_squared_error(self.y_train, train_pred))),
                "test_rmse": float(np.sqrt(mean_squared_error(self.y_test, test_pred))),
                "train_mae": float(mean_absolute_error(self.y_train, train_pred)),
                "test_mae": float(mean_absolute_error(self.y_test, test_pred))
            }
        }
    
    def get_feature_importance(self):
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        importance = self.model.feature_importances_
        feature_importance = [
            {"feature": name, "importance": float(imp)}
            for name, imp in zip(self.feature_names, importance)
        ]                
        feature_importance.sort(key=lambda x: x["importance"], reverse=True)        
        return feature_importance
    
    def get_sample_data(self, n_samples=5):
        indices = np.random.choice(len(self.X_test), n_samples, replace=False)
        samples = []
        
        for idx in indices:
            sample = {
                "features": {
                    name: float(value)
                    for name, value in zip(self.feature_names, self.X_test[idx])
                },
                "actual_price": float(self.y_test[idx]),
                "actual_price_thousands": float(self.y_test[idx] * 100)
            }
            
            # Add prediction
            pred = self.predict(self.X_test[idx].reshape(1, -1))
            sample["predicted_price"] = float(pred[0])
            sample["predicted_price_thousands"] = float(pred[0] * 100)            
            samples.append(sample)        
        return samples
