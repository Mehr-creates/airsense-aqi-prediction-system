import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class FeatureStoreManager:
    """
    Manages connections and transactions with the Feature Store.
    Currently running in demo/mock mode for generating placeholder data.
    """
    def __init__(self):
        # Placeholders for actual feature store client and project
        self.project = None
        self.fs = None
        
    def initialize_connection(self):
        """
        Initialize feature store connection.
        Returns True on simulated success, False on error.
        """
        try:
            # For demo purposes, we'll simulate a successful connection
            print("Connected to feature store (demo mode)")
            return True
        except Exception as e:
            print(f"Feature store connection failed: {e}")
            return False
    
    def create_feature_group(self, feature_data, feature_group_name="aqi_features"):
        """
        Create or retrieve an existing feature group to store AQI data.
        """
        try:
            print(f"Creating feature group: {feature_group_name}")
            print(f"Inserted {len(feature_data)} records")
            return True
        except Exception as e:
            print(f"Feature group creation failed: {e}")
            return None
    
    def get_historical_features(self, feature_group_name="aqi_features", days=30):
        """Get historical features from feature store (demo version)"""
        try:
            return self._generate_sample_features(days)
        except Exception as e:
            print(f"Feature retrieval failed: {e}")
            return self._generate_sample_features(days)
    
    def _generate_sample_features(self, days=30):
        """
        Generates simulated historical feature data for demonstration purposes.
        Creates records across given 'days' for a sample subset of cities.
        """
        dates = [datetime.now() - timedelta(days=x) for x in range(days)]
        cities = ["Delhi", "Ghaziabad", "Kanpur"]
        
        features = []
        for date in dates:
            for city in cities:
                # Generate a randomized baseline AQI score (1 to 5 scale)
                base_aqi = np.random.normal(2.5, 0.8)
                
                features.append({
                    'city': city,
                    'timestamp': date,
                    'aqi': max(1, min(5, base_aqi)), # Clip to valid scale
                    'pm2_5': max(0, np.random.normal(35, 15)),
                    'pm10': max(0, np.random.normal(55, 20)),
                    'no2': max(0, np.random.normal(25, 10)),
                    'so2': max(0, np.random.normal(12, 5)),
                    'co': max(0, np.random.normal(250, 100)),
                    'o3': max(0, np.random.normal(45, 15)),
                    'temperature': np.random.normal(25, 5),
                    'humidity': np.random.normal(60, 15),
                    'wind_speed': np.random.normal(15, 5),
                    'pressure': np.random.normal(1013, 10),
                    'is_hazardous': 1 if base_aqi >= 4 else 0 # Flag hazardous if AQI >= 4
                })
        
        return pd.DataFrame(features)