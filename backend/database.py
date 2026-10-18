import sqlite3
import pandas as pd
from config.settings import DB_PATH
from datetime import datetime

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS air_quality (
            timestamp_utc TEXT UNIQUE, pm25 REAL, source_type TEXT, source_name TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS weather (
            timestamp_utc TEXT UNIQUE, temperature_2m REAL, relative_humidity_2m REAL, 
            wind_speed_10m REAL, source_type TEXT, source_name TEXT)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS model_experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp_run TEXT, model_name TEXT, 
            mae REAL, rmse REAL)""")
        conn.commit()

def insert_data(table: str, df: pd.DataFrame):
    if df.empty: return
    with get_connection() as conn:
        df.to_sql(table, conn, if_exists='append', index=False)
        conn.commit()

def get_joined_data():
    with get_connection() as conn:
        query = """
            SELECT a.timestamp_utc, a.pm25, a.source_type as aq_source, 
                   w.temperature_2m, w.relative_humidity_2m, w.wind_speed_10m 
            FROM air_quality a 
            LEFT JOIN weather w ON a.timestamp_utc = w.timestamp_utc 
            ORDER BY a.timestamp_utc ASC
        """
        df = pd.read_sql(query, conn)
    if not df.empty:
        df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
        df['hour'] = df['timestamp_utc'].dt.hour
        df['day_of_week'] = df['timestamp_utc'].dt.day_name()
    return df

def save_experiment(model_name, mae, rmse):
    with get_connection() as conn:
        conn.execute("INSERT INTO model_experiments (timestamp_run, model_name, mae, rmse) VALUES (?, ?, ?, ?)",
                     (datetime.utcnow().isoformat(), model_name, mae, rmse))
        conn.commit()

def get_experiments():
    with get_connection() as conn:
        try: return pd.read_sql("SELECT * FROM model_experiments ORDER BY timestamp_run DESC", conn)
        except: return pd.DataFrame()

init_db()
