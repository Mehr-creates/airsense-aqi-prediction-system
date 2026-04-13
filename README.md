AQI Predictor Dashboard

Author: Mehr Chawla
Tech Stack: Python, Streamlit, Machine Learning, TensorFlow, OpenWeather API

Table of Contents
Overview
Features
System Architecture
Installation
Usage
Machine Learning Models
Project Structure
Results & Performance
Contributing
Support & Contact
Acknowledgments
Overview

AirSense is a real-time Air Quality Index (AQI) monitoring and short-term prediction system designed to make air quality data easier to understand and act on.Most systems only display current AQI levels, while AirSense extends functionality by predicting future AQI values using machine learning and deep learning models.It integrates live weather data, historical pollution data, and time-series modeling to generate reliable short-term forecasts.

The system uses XGBoost and LightGBM for structured prediction tasks and an LSTM model for time-based forecasting.Results are visualized through an interactive Streamlit dashboard that enables users to explore pollutant trends, monitor AQI changes, and view predictive outputs.

AirSense was developed as both an academic research project and a functional prototype for intelligent environmental monitoring systems.

Features
Real-time AQI monitoring using live environmental data
Short-term AQI prediction using machine learning models
Time-series forecasting using LSTM neural networks
Hybrid modeling approach using XGBoost, LightGBM, and LSTM
Interactive Streamlit dashboard for visualization
Offline training pipeline for model retraining
Data preprocessing and feature engineering workflow
Modular architecture supporting scalability and extension
API-based environmental data integration
Visual trend analysis for pollutant levels
System Architecture

AirSense follows a modular pipeline that separates data ingestion, processing, modeling, and visualization to improve maintainability and scalability.

Workflow Overview
Data Collection
Environmental and weather data fetched from APIs such as OpenWeatherMap
Historical AQI datasets used for model training
Data Preprocessing
Handling missing values
Feature engineering
Data scaling and normalization
Dataset formatting for ML and LSTM models
Model Training
XGBoost and LightGBM trained on structured features
LSTM trained on sequential time-series data
Trained models saved for reuse during inference
Prediction Layer
Processed live data passed into trained models
Short-term AQI predictions generated
Visualization Layer

Streamlit dashboard displays:

Current AQI
Historical trends
Predicted AQI values
Pollutant comparisons
Installation
1. Clone the Repository
git clone https://github.com/Mehr-creates/airsense-aqi-prediction-system.git
cd airsense-aqi-prediction-system
2. Create Virtual Environment
python -m venv venv

Activate the environment:

Mac/Linux

source venv/bin/activate

Windows

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure API Keys

Create a .env file and add your API credentials:

OPENWEATHER_API_KEY=your_api_key_here
5. Run the Dashboard
streamlit run app.py

The dashboard will open automatically in your browser.

6. Train Models (Optional)

To retrain the LSTM model offline:

python offline_lstm_training.py
Usage

After launching the dashboard, users can:

View current AQI values
Explore pollutant trends
Analyze historical air quality data
Generate short-term AQI predictions
Compare pollutant levels across time
Machine Learning Models

AirSense integrates multiple machine learning and deep learning models to improve predictive accuracy and reliability.

XGBoost

Used for structured prediction tasks involving engineered features.Provides strong performance on tabular environmental datasets.

LightGBM

Optimized gradient boosting model that improves training speed and scalability while maintaining prediction accuracy.

LSTM (Long Short-Term Memory)

Deep learning model designed for time-series forecasting.Enables sequential learning from historical AQI patterns and improves temporal prediction accuracy.

Project Structure
aqi-dashboard/

├── app.py
├── offline_lstm_training.py
├── generate_revised_diagrams.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore

├── .streamlit/
│   └── config.toml

├── data/
│   ├── raw/
│   ├── processed/

├── models/
│   ├── xgboost_model.pkl
│   ├── lightgbm_model.pkl
│   ├── lstm_model.h5

├── utils/
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── prediction.py
│   ├── visualization.py
Results & Performance

The hybrid modeling approach improves predictive robustness by combining structured learning and sequential forecasting techniques.Model outputs demonstrate reliable short-term AQI prediction capability across varying environmental conditions.Performance evaluation includes error metrics such as RMSE and MAE along with visualization-based validation.

Contributing

Contributions are welcome.To contribute:

Fork the repository
Create a new feature branch
Commit your changes
Submit a pull request
Support & Contact

For questions, feedback, or collaboration opportunities, contact:

Mehr Chawla
Email: mehrchawla314@gmail.com

GitHub: https://github.com/Mehr-creates

Acknowledgments

This project utilizes open-source libraries and publicly available environmental datasets.Special acknowledgment to developers of Streamlit, TensorFlow, XGBoost, LightGBM, and OpenWeatherMap API for enabling rapid development of predictive environmental systems.