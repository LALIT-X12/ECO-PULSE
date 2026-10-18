import streamlit as st
from config.settings import DEMO_MODE
from backend.data_fetcher import run_pipeline

# Import frontend modules
from frontend.dashboard import render as render_dashboard
from frontend.analytics import render as render_analytics
from frontend.research_lab import render as render_research
from frontend.trust_view import render as render_trust

st.set_page_config(page_title="EcoPulse", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    h1, h2, h3 { color: #00BFA5 !important; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🌿 EcoPulse")

if DEMO_MODE:
    st.sidebar.warning("⚠️ DEMO MODE: No API Key found.")

if st.sidebar.button("📡 Fetch Live Data"):
    with st.spinner("Fetching..."):
        run_pipeline()
        st.sidebar.success("Data updated!")

page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "📊 Analytics", 
    "🔬 Research Lab", 
    "🛡️ Trust Engine"
])

if page == "🏠 Dashboard":
    render_dashboard()
elif page == "📊 Analytics":
    render_analytics()
elif page == "🔬 Research Lab":
    render_research()
elif page == "🛡️ Trust Engine":
    render_trust()
