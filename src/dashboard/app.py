import streamlit as st

from views import (
    home,
    profile,
    screener,
    peers,
    trends,
    sectors,
    capital,
    reports,
)

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
    "🏠 Home": home,
    "🏢 Company Profile": profile,
    "🔎 Screener": screener,
    "👥 Peer Comparison": peers,
    "📈 Trend Analysis": trends,
    "🏭 Sector Analysis": sectors,
    "💰 Capital Allocation": capital,
    "📄 Annual Reports": reports,
}

choice = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys())
)

PAGES[choice].show()