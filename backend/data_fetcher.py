import requests
import pandas as pd
import numpy as np
from config.settings import OPENAQ_API_KEY, DEMO_MODE, CHENNAI_LAT, CHENNAI_LON

def fetch_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={CHENNAI_LAT}&longitude={CHENNAI_LON}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&past_days=7&timezone=UTC"
    res = requests.get(url).json()['hourly']
    df = pd.DataFrame(res).rename(columns={"time": "timestamp_utc"})
    df['source_type'] = 'reanalysis'
    df['source_name'] = 'Open-Meteo'
    return df

def fetch_air_quality():
    if DEMO_MODE:
        dates = pd.date_range(end=pd.Timestamp.utcnow(), periods=168, freq='h').strftime('%Y-%m-%dT%H:%M:%SZ')
        return pd.DataFrame({
            "timestamp_utc": dates,
            "pm25": np.random.normal(45, 15, len(dates)).clip(10, 150),
            "source_type": "synthetic",
            "source_name": "Demo Generator"
        })
    
    # If API key exists, fetch real data (Simplified for structure)
    # In production, you would query OpenAQ v3 endpoints here
    return pd.DataFrame()

def run_pipeline():
    from backend.database import insert_data
    w_df = fetch_weather()
    aq_df = fetch_air_quality()
    
    # Simple cleaning
    for df in [w_df, aq_df]:
        if not df.empty:
            df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            df.drop_duplicates(subset=['timestamp_utc'], inplace=True)
            
    insert_data('weather', w_df)
    insert_data('air_quality', aq_df)
