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
    valuation,
    ai_insights,
)

st.set_page_config(
    page_title="Nifty 100 Financial Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
    "🏠 Home": home,
    "🏢 Company Profile": profile,
    "🔎 Stock Screener": screener,
    "👥 Peer Comparison": peers,
    "📈 Trend Analysis": trends,
    "🏭 Sector Analysis": sectors,
    "💰 Capital Allocation": capital,
    "💹 Valuation": valuation,
    "🤖 AI Insights": ai_insights,
    "📄 Annual Reports": reports,
}

st.sidebar.title("📊 Navigation")

choice = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys()),
    label_visibility="collapsed",
)

PAGES[choice].show()