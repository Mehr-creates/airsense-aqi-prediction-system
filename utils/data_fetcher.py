import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class AQIDataFetcher:
    """
    Handles fetching and simulating Air Quality Index (AQI) and meteorological data for various cities.
    In a full production environment, this replaces simulated values with direct OpenWeatherMap API responses.
    """
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # City-specific base AQI patterns (realistic averages)
        # These profiles define geographical baselines for pollution and variation
        self.city_profiles = {
            "Delhi": {"base_aqi": 4.5, "variation": 0.5, "industrial": True, "traffic": "very_high"},
            "Ghaziabad": {"base_aqi": 4.3, "variation": 0.6, "industrial": True, "traffic": "very_high"},
            "Kanpur": {"base_aqi": 4.0, "variation": 0.5, "industrial": True, "traffic": "high"},
            "Ludhiana": {"base_aqi": 3.8, "variation": 0.4, "industrial": True, "traffic": "high"},
            "Mumbai": {"base_aqi": 3.5, "variation": 0.5, "industrial": True, "traffic": "very_high"},
            "Bangalore": {"base_aqi": 2.8, "variation": 0.4, "industrial": False, "traffic": "high"},
            "Chennai": {"base_aqi": 3.0, "variation": 0.4, "industrial": True, "traffic": "high"},
            "Hyderabad": {"base_aqi": 3.2, "variation": 0.4, "industrial": True, "traffic": "high"},
            "Shillong": {"base_aqi": 1.8, "variation": 0.3, "industrial": False, "traffic": "low"},
            "Goa": {"base_aqi": 2.0, "variation": 0.3, "industrial": False, "traffic": "low"}
        }
        
    def get_city_coordinates(self, city_name):
        """Get coordinates for a city"""
        city_coordinates = {
            "Delhi": (28.6139, 77.2090),
            "Ghaziabad": (28.6692, 77.4538),
            "Kanpur": (26.4499, 80.3319),
            "Ludhiana": (30.9010, 75.8573),
            "Mumbai": (19.0760, 72.8777),
            "Bangalore": (12.9716, 77.5946),
            "Chennai": (13.0827, 80.2707),
            "Hyderabad": (17.3850, 78.4867),
            "Shillong": (25.5788, 91.8933),
            "Goa": (15.2993, 74.1240)
        }
        
        return city_coordinates.get(city_name, (28.6139, 77.2090))
    
    def get_current_aqi(self, lat, lon, city_name="Delhi"):
        """Get current AQI data - city-specific"""
        return self._generate_city_specific_current_data(city_name)
    
    def get_historical_aqi(self, lat, lon, city_name="Delhi", days=30):
        """Get historical AQI data with city-specific patterns"""
        return self._generate_city_specific_historical_data(city_name, days)
    
    def _generate_city_specific_current_data(self, city_name):
        """
        Generate realistic current AQI data specific to each city.
        Takes into account the city's geographical/industrial profile.
        """
        profile = self.city_profiles.get(city_name, self.city_profiles["Delhi"])
        
        # Base AQI with city-specific pattern and some randomness 
        # (simulating real-world minute-by-minute fluctuations)
        base_aqi = np.random.normal(profile["base_aqi"], profile["variation"])
        base_aqi = max(1.0, min(5.0, base_aqi))
        
        # City-specific pollutant patterns
        if city_name == "Delhi":
            # Delhi typically has very high PM2.5 and PM10
            pm25 = base_aqi * 14 + np.random.normal(0, 4)
            pm10 = base_aqi * 28 + np.random.normal(0, 6)
            no2 = base_aqi * 9 + np.random.normal(0, 3)
        elif city_name == "Ghaziabad":
            # Ghaziabad has heavy industrial pollution
            pm25 = base_aqi * 13 + np.random.normal(0, 4)
            pm10 = base_aqi * 26 + np.random.normal(0, 6)
            no2 = base_aqi * 8 + np.random.normal(0, 3)
        elif city_name == "Kanpur":
            # Kanpur has industrial and vehicular pollution
            pm25 = base_aqi * 12 + np.random.normal(0, 3)
            pm10 = base_aqi * 24 + np.random.normal(0, 5)
            no2 = base_aqi * 7 + np.random.normal(0, 2)
        elif city_name == "Shillong":
            # Shillong has cleaner air (hill station)
            pm25 = base_aqi * 5 + np.random.normal(0, 1)
            pm10 = base_aqi * 10 + np.random.normal(0, 2)
            no2 = base_aqi * 3 + np.random.normal(0, 1)
        elif city_name == "Goa":
            # Goa has relatively clean coastal air
            pm25 = base_aqi * 6 + np.random.normal(0, 2)
            pm10 = base_aqi * 11 + np.random.normal(0, 3)
            no2 = base_aqi * 3 + np.random.normal(0, 1)
        else:
            # Other cities
            pm25 = base_aqi * 9 + np.random.normal(0, 3)
            pm10 = base_aqi * 18 + np.random.normal(0, 4)
            no2 = base_aqi * 6 + np.random.normal(0, 2)
        
        return {
            'aqi': round(base_aqi, 1),
            'pm2_5': round(max(5, pm25), 1),
            'pm10': round(max(10, pm10), 1),
            'no2': round(max(2, no2), 1),
            'so2': round(max(1, base_aqi * 3 + np.random.normal(0, 1)), 1),
            'co': round(max(50, base_aqi * 70 + np.random.normal(0, 20)), 1),
            'o3': round(max(5, base_aqi * 10 + np.random.normal(0, 3)), 1),
            'timestamp': datetime.now(),
            'temperature': self._get_city_temperature(city_name),
            'humidity': self._get_city_humidity(city_name),
            'wind_speed': self._get_city_wind_speed(city_name),
            'pressure': round(np.random.normal(1013, 10), 1),
            'city': city_name
        }
    
    def _generate_city_specific_historical_data(self, city_name, days=30):
        """Generate realistic historical data with city-specific trends"""
        profile = self.city_profiles.get(city_name, self.city_profiles["Delhi"])
        dates = [datetime.now() - timedelta(days=x) for x in range(days, 0, -1)]
        
        # Create city-specific patterns
        data = []
        for i, date in enumerate(dates):
            # Weekly pattern (worse on weekdays)
            day_of_week = date.weekday()
            weekday_factor = 1.2 if day_of_week < 5 else 0.8
            
            # Seasonal pattern (slight variation)
            seasonal_factor = 1 + 0.1 * np.sin(i * 0.05)
            
            # City-specific base with trends
            base_aqi = profile["base_aqi"] * seasonal_factor * weekday_factor
            base_aqi += np.random.normal(0, profile["variation"])
            base_aqi = max(1.0, min(5.0, base_aqi))
            
            # City-specific pollutant calculations
            if city_name == "Delhi":
                pm25 = base_aqi * 14 + np.random.normal(0, 4)
                pm10 = base_aqi * 28 + np.random.normal(0, 6)
            elif city_name == "Ghaziabad":
                pm25 = base_aqi * 13 + np.random.normal(0, 4)
                pm10 = base_aqi * 26 + np.random.normal(0, 6)
            elif city_name == "Kanpur":
                pm25 = base_aqi * 12 + np.random.normal(0, 3)
                pm10 = base_aqi * 24 + np.random.normal(0, 5)
            elif city_name == "Shillong":
                pm25 = base_aqi * 5 + np.random.normal(0, 1)
                pm10 = base_aqi * 10 + np.random.normal(0, 2)
            elif city_name == "Goa":
                pm25 = base_aqi * 6 + np.random.normal(0, 2)
                pm10 = base_aqi * 11 + np.random.normal(0, 3)
            else:
                pm25 = base_aqi * 9 + np.random.normal(0, 3)
                pm10 = base_aqi * 18 + np.random.normal(0, 4)
            
            data.append({
                'date': date.date(),
                'aqi': round(base_aqi, 2),
                'pm2_5': round(max(5, pm25), 1),
                'pm10': round(max(10, pm10), 1),
                'no2': round(max(2, base_aqi * 6 + np.random.normal(0, 2)), 1),
                'so2': round(max(1, base_aqi * 3 + np.random.normal(0, 1)), 1),
                'co': round(max(50, base_aqi * 70 + np.random.normal(0, 20)), 1),
                'o3': round(max(5, base_aqi * 10 + np.random.normal(0, 3)), 1),
                'city': city_name
            })
        
        return pd.DataFrame(data)
    
    def _get_city_temperature(self, city_name):
        """Get city-specific temperature patterns"""
        temp_profiles = {
            "Delhi": (25, 10),     # mean, variation (extreme seasons)
            "Ghaziabad": (25, 10), # similar to Delhi
            "Kanpur": (26, 9),     # hot summers
            "Ludhiana": (24, 10),  # continental climate
            "Mumbai": (27, 3),     # tropical, stable
            "Bangalore": (24, 3),  # pleasant, mild
            "Chennai": (29, 3),    # hot, tropical
            "Hyderabad": (27, 5),  # warm, semi-arid
            "Shillong": (17, 5),   # cool hill station
            "Goa": (28, 3)         # tropical coastal
        }
        mean_temp, variation = temp_profiles.get(city_name, (25, 8))
        return round(np.random.normal(mean_temp, variation), 1)
    
    def _get_city_humidity(self, city_name):
        """Get city-specific humidity patterns"""
        humidity_profiles = {
            "Delhi": (55, 20),      # varies widely by season
            "Ghaziabad": (55, 18),  # similar to Delhi
            "Kanpur": (58, 18),     # moderate humidity
            "Ludhiana": (60, 15),   # moderate
            "Mumbai": (75, 10),     # very humid (coastal)
            "Bangalore": (60, 12),  # moderate
            "Chennai": (72, 10),    # humid (coastal)
            "Hyderabad": (55, 15),  # moderate
            "Shillong": (78, 10),   # very humid (hills)
            "Goa": (73, 10)         # humid (coastal)
        }
        mean_humidity, variation = humidity_profiles.get(city_name, (60, 15))
        return round(max(20, min(95, np.random.normal(mean_humidity, variation))), 1)
    
    def _get_city_wind_speed(self, city_name):
        """Get city-specific wind speed patterns"""
        wind_profiles = {
            "Delhi": (10, 4),       # moderate
            "Ghaziabad": (9, 4),    # similar to Delhi
            "Kanpur": (10, 4),      # moderate
            "Ludhiana": (8, 3),     # mild
            "Mumbai": (16, 6),      # windy (coastal)
            "Bangalore": (12, 4),   # moderate
            "Chennai": (14, 5),     # coastal winds
            "Hyderabad": (11, 4),   # moderate
            "Shillong": (10, 5),    # hill breezes
            "Goa": (15, 5)          # coastal winds
        }
        mean_wind, variation = wind_profiles.get(city_name, (12, 4))
        return round(max(2, np.random.normal(mean_wind, variation)), 1)