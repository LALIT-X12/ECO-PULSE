import pandas as pd
from datetime import datetime, timezone
from sklearn.ensemble import IsolationForest

def calculate_quality_score(df: pd.DataFrame):
    if df.empty: return {"score": 0, "details": ["No data"]}
    
    score = 100.0
    details = []
    
    # Completeness
    missing = df[['pm25', 'temperature_2m']].isnull().sum().sum()
    if missing > 0:
        score -= 20
        details.append(f"Missing {missing} values.")
        
    # Freshness
    latest = pd.to_datetime(df['timestamp_utc']).max()
    if latest.tzinfo is None: latest = latest.replace(tzinfo=timezone.utc)
    hours_old = (datetime.now(timezone.utc) - latest).total_seconds() / 3600
    if hours_old > 3:
        score -= 20
        details.append(f"Data is {hours_old:.1f} hours old.")
        
    # Source
    if 'synthetic' in df['aq_source'].unique():
        score -= 50
        details.append("Contains synthetic data.")
        
    return {"score": max(0, score), "details": details}

def detect_anomalies(df: pd.DataFrame):
    if len(df) < 20: return df
    
    iso = IsolationForest(contamination=0.05, random_state=42)
    features = ['pm25', 'temperature_2m', 'wind_speed_10m']
    
    # Fit and predict
    preds = iso.fit_predict(df[features].fillna(0))
    df['is_anomaly'] = preds == -1
    return df
