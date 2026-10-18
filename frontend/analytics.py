import streamlit as st
import plotly.express as px
from backend.database import get_joined_data

def render():
    st.title("📊 Exploratory Analytics")
    df = get_joined_data()
    if df.empty: return st.warning("No data available.")
    
    tab1, tab2 = st.tabs(["Hourly Patterns", "Weather Correlation"])
    
    with tab1:
        hourly = df.groupby('hour')['pm25'].mean().reset_index()
        fig = px.line(hourly, x='hour', y='pm25', markers=True, template="plotly_dark", title="Avg PM2.5 by Hour")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        fig = px.scatter(df, x='temperature_2m', y='pm25', trendline="ols", template="plotly_dark", title="Temp vs PM2.5")
        st.plotly_chart(fig, use_container_width=True)
