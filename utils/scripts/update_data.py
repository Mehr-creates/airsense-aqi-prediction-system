#!/usr/bin/env python3
"""
Automated data update script for GitHub Actions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_fetcher import AQIDataFetcher
from utils.feature_store import FeatureStoreManager
import pandas as pd
from datetime import datetime

def main():
    print("Starting automated data update...")
    
    # Initialize components
    data_fetcher = AQIDataFetcher()
    feature_store = FeatureStoreManager()
    
    # Cities to monitor
    cities = ["Delhi", "Ghaziabad", "Kanpur", "Ludhiana", "Mumbai"]
    
    all_data = []
    
    # Iterate through target cities to fetch current live data
    for city in cities:
        print(f"Fetching data for {city}...")
        
        # Retrieve geological coordinates for the given city
        lat, lon = data_fetcher.get_city_coordinates(city)
        
        if lat and lon:
            # Fetch the live AQI representation using coordinates
            current_data = data_fetcher.get_current_aqi(lat, lon)
            current_data['city'] = city
            current_data['timestamp'] = datetime.now()
            
            all_data.append(current_data)
    
    # Push aggregated data to the feature store
    if all_data:
        # Convert dictionary list to pandas DataFrame
        feature_df = pd.DataFrame(all_data)
        
        # Save structured data to feature registry
        feature_store.create_feature_group(feature_df)
        print(f"Successfully updated data for {len(all_data)} cities")
    else:
        print("No data was fetched successfully")

if __name__ == "__main__":
    main()