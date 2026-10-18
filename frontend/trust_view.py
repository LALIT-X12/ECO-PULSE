import streamlit as st
import plotly.express as px
from backend.database import get_joined_data
from backend.trust_engine import calculate_quality_score, detect_anomalies

def render():
    st.title("🛡️ Forecast Trust Engine")
    df = get_joined_data()
    if df.empty: return st.warning("No data.")
    
    # 1. Quality Score
    score_data = calculate_quality_score(df)
    st.metric("Data Quality Score", f"{score_data['score']}/100")
    for d in score_data['details']:
        st.write(f"- {d}")
        
    st.divider()
    
    # 2. Anomalies
    st.subheader("Anomaly Detection")
    df_anom = detect_anomalies(df)
    anomalies = df_anom[df_anom['is_anomaly'] == True]
    
    if not anomalies.empty:
        st.warning(f"Detected {len(anomalies)} anomaly candidates.")
        fig = px.scatter(df_anom, x='timestamp_utc', y='pm25', color='is_anomaly', 
                         color_discrete_map={True: 'red', False: '#00BFA5'}, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No anomalies detected.")
