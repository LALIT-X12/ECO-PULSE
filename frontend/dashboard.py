import streamlit as st
import plotly.express as px
from backend.database import get_joined_data

def render():
    st.title("Environmental Intelligence Overview")
    df = get_joined_data()
    
    if df.empty:
        st.warning("No data. Go to the sidebar and click 'Fetch Live Data'.")
        return
        
    latest = df.iloc[-1]
    st.markdown(f"Data Status: `{latest['aq_source'].upper()}` | Last Updated: {latest['timestamp_utc']}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("PM2.5", f"{latest['pm25']:.1f} µg/m³")
    col2.metric("Temperature", f"{latest['temperature_2m']:.1f} °C")
    col3.metric("Wind Speed", f"{latest['wind_speed_10m']:.1f} km/h")
    
    st.subheader("Recent PM2.5 Trends")
    fig = px.line(df.tail(48), x='timestamp_utc', y='pm25', template="plotly_dark")
    fig.update_traces(line_color='#00BFA5')
    st.plotly_chart(fig, use_container_width=True)
