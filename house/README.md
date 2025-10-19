# 🏠 House Price Prediction App

A beautiful and interactive web application for predicting house prices using Machine Learning. Built with FastAPI backend and modern responsive UI, using the California Housing dataset from scikit-learn.

## ✨ Features

- **Real-time Price Prediction**: Predict house prices based on 8 key features
- **Interactive UI**: Modern, responsive design with gradient themes
- **Model Information**: View detailed model performance metrics
- **Sample Data**: Explore sample predictions from the dataset
- **Feature Importance**: Visualize which features matter most
- **Model Retraining**: Retrain the model with a single click
- **RESTful API**: Well-documented API endpoints

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd house
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser**
   
   Navigate to: `http://localhost:8000`

3. **Explore the API documentation**
   
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## 📊 Dataset Information

The app uses the **California Housing Dataset** from scikit-learn, which contains:

- **20,640 samples** from the 1990 California census
- **8 features**:
  - `MedInc`: Median income in block group
  - `HouseAge`: Median house age in block group
  - `AveRooms`: Average number of rooms per household
  - `AveBedrms`: Average number of bedrooms per household
  - `Population`: Block group population
  - `AveOccup`: Average number of household members
  - `Latitude`: Block group latitude
  - `Longitude`: Block group longitude
- **Target**: Median house value (in $100,000s)

## 🎯 How to Use

### Web Interface

1. **Prediction Tab**: 
   - Enter house features manually or click "Random Example"
   - Click "Predict Price" to get the prediction
   - View the predicted price in a beautiful result card

2. **Model Info Tab**:
   - View model architecture and parameters
   - See performance metrics (R², RMSE, MAE)
   - Retrain the model if needed

3. **Sample Data Tab**:
   - Load random samples from the test set
   - Compare actual vs predicted prices
   - Explore feature values

4. **Feature Importance Tab**:
   - Visual bars showing which features are most important
   - Sorted by importance score

### API Endpoints

#### Predict House Price
```bash
POST /predict
Content-Type: application/json

{
  "MedInc": 3.5,
  "HouseAge": 25.0,
  "AveRooms": 5.5,
  "AveBedrms": 1.2,
  "Population": 1500.0,
  "AveOccup": 3.0,
  "Latitude": 37.5,
  "Longitude": -122.0
}
```

#### Get Dataset Info
```bash
GET /dataset-info
```

#### Get Model Info
```bash
GET /model-info
```

#### Get Sample Data
```bash
GET /sample-data
```

#### Get Feature Importance
```bash
GET /feature-importance
```

#### Retrain Model
```bash
POST /retrain
```

## 🏗️ Project Structure

```
house/
├── main.py              # FastAPI application with endpoints
├── model.py             # ML model class and training logic
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── house_price_model.pkl   # Trained model (generated)
├── scaler.pkl          # Feature scaler (generated)
└── static/             # Frontend files
    ├── index.html      # Main HTML page
    ├── styles.css      # Styling
    └── script.js       # JavaScript for interactivity
```

## 🤖 Model Details

- **Algorithm**: Random Forest Regressor
- **Estimators**: 100 trees
- **Max Depth**: 20
- **Features**: Scaled using StandardScaler
- **Performance**: 
  - Test R² Score: ~0.80-0.82
  - Test RMSE: ~0.48-0.52
  - Test MAE: ~0.32-0.35

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Beautiful Gradients**: Purple gradient theme
- **Smooth Animations**: Fade-in effects and transitions
- **Interactive Forms**: Real-time validation
- **Data Visualization**: Feature importance bars
- **Notifications**: Toast messages for user feedback

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework
- **scikit-learn**: Machine learning library
- **Pydantic**: Data validation
- **NumPy**: Numerical computing
- **Joblib**: Model serialization

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No frameworks needed
- **Fetch API**: Async HTTP requests

## 📝 Example Usage

```python
import requests

# Predict house price
features = {
    "MedInc": 3.5,
    "HouseAge": 25.0,
    "AveRooms": 5.5,
    "AveBedrms": 1.2,
    "Population": 1500.0,
    "AveOccup": 3.0,
    "Latitude": 37.5,
    "Longitude": -122.0
}

response = requests.post("http://localhost:8000/predict", json=features)
result = response.json()

print(f"Predicted Price: ${result['price_in_thousands']:.2f}k")
```

## 🔧 Customization

### Change Model Parameters

Edit `model.py` in the `train()` method:

```python
self.model = RandomForestRegressor(
    n_estimators=200,  # Increase trees
    max_depth=25,      # Deeper trees
    random_state=42
)
```

### Modify UI Theme

Edit `static/styles.css` CSS variables:

```css
:root {
    --primary-color: #4f46e5;  /* Change primary color */
    --secondary-color: #10b981; /* Change secondary color */
}
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --port 8080
```

### Model Not Found
The model will be automatically trained on first run. If you encounter issues:
```bash
# Delete existing model files
rm house_price_model.pkl scaler.pkl

# Restart the server to retrain
python main.py
```

### Dependencies Issues
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## 📈 Future Enhancements

- [ ] Add more ML models (XGBoost, LightGBM)
- [ ] Model comparison feature
- [ ] Historical predictions tracking
- [ ] Export predictions to CSV
- [ ] Dark mode toggle
- [ ] More visualization charts
- [ ] Batch prediction upload

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📧 Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ using FastAPI and scikit-learn**
