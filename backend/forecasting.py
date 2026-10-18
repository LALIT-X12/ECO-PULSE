import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from backend.database import save_experiment

def train_and_evaluate(df: pd.DataFrame):
    df = df.sort_values('timestamp_utc').copy()
    
    # Feature Engineering
    df['target'] = df['pm25'].shift(-1)
    df['lag_1'] = df['pm25'].shift(1)
    df['lag_24'] = df['pm25'].shift(24)
    df = df.dropna()
    
    if len(df) < 20: return None

    X = df[['lag_1', 'lag_24', 'temperature_2m', 'hour']]
    y = df['target']
    
    # Chronological Split
    split = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    
    # Baseline (Persistence)
    base_preds = X_test['lag_1']
    base_mae = mean_absolute_error(y_test, base_preds)
    save_experiment("Baseline", base_mae, np.sqrt(mean_squared_error(y_test, base_preds)))
    
    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_preds)
    save_experiment("Random Forest", rf_mae, np.sqrt(mean_squared_error(y_test, rf_preds)))
    
    return {
        "baseline_mae": base_mae,
        "rf_mae": rf_mae,
        "features": X.columns.tolist(),
        "importances": rf.feature_importances_,
        "dates": df.iloc[split:]['timestamp_utc'],
        "actual": y_test,
        "preds": rf_preds
    }
