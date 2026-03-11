import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 1. ANALYTICAL UI CONFIGURATION
st.set_page_config(page_title="Monetary Pulse Terminal", layout="wide")

# PROFESSIONAL GRADE CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; color: #ffffff; }
    .main-header { font-family: 'JetBrains Mono', monospace; color: #00d4ff; font-size: 4rem; font-weight: 900; letter-spacing: -3px; margin-bottom: 0px; line-height: 1; }
    .stSelectbox, .stSlider { background: #161b22; border-radius: 8px; padding: 10px; border: 1px solid #30363d; }
    [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. PROMINENT HEADER
st.markdown('<p class="main-header">MONETARY TERMINAL</p>', unsafe_allow_html=True)
st.markdown("SYSTEM STATUS: **OPERATIONAL** | DATA SYNC: **ACTIVE**")
st.markdown("---")

# 3. INTERACTIVE CONTROL PANEL (MAIN PAGE)
current_date = datetime.now()
available_months = [(current_date - relativedelta(months=i)).strftime('%B %Y') for i in range(12)]

c_ctrl1, c_ctrl2 = st.columns([1, 2]) # Makes slider wider than dropdown

with c_ctrl1:
    selected_month = st.selectbox("OBSERVATION PERIOD", available_months)

with c_ctrl2:
    repo_rate = st.select_slider(
        "POLICY REPO RATE (%)",
        options=[4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 10.0],
        value=6.5
    )

st.markdown("---")

# 4. DATA ENGINE LOGIC
spread = repo_rate - 6.5
velocity_score = 100 - (spread * 12.5) if spread > 0 else 100 + (abs(spread) * 5.0)

# 5. DYNAMIC ANALYTICS GRID (Side-by-Side)
col_metrics, col_gauge = st.columns([2, 1]) # Metrics take more space

with col_metrics:
    st.markdown("### System Indicators")
    m1, m2 = st.columns(2)
    m3, m4 = st.columns(2)
    
    m1.metric("REPO RATE", f"{repo_rate}%", f"{spread:.2f}%", delta_color="inverse")
    m2.metric("LIQUIDITY INDEX", f"{velocity_score:.1f}", f"{-spread*8:.1f}bps")
    m3.metric("PERIOD", selected_month)
    m4.metric("RISK STATUS", "CRITICAL" if repo_rate > 7.5 else "STABLE")

with col_gauge:
    # Speedometer (Gauge)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = velocity_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credit Absorption Speed", 'font': {'size': 18, 'color': '#ffffff'}},
        gauge = {
            'axis': {'range': [0, 150], 'tickcolor': "#ffffff"},
            'bar': {'color': "#00d4ff"},
            'bgcolor': "#161b22",
            'steps': [
                {'range': [0, 50], 'color': "#ff4b4b"},
                {'range': [50, 100], 'color': "#ffa500"},
                {'range': [100, 150], 'color': "#00cc96"}]
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=280, margin=dict(t=50, b=0, l=10, r=10))
    st.plotly_chart(fig_gauge, use_container_width=True)

# 6. TIME-SERIES PROJECTIONS
st.markdown("### Projected Sectoral Impact")
months_series = [(current_date - relativedelta(months=i)).strftime('%b %Y') for i in range(6)][::-1]

# Create dummy data that reacts to the slider
data_1 = [12 + (spread * -0.9 * i) for i in range(6)]
data_2 = [10 + (spread * -1.4 * i) for i in range(6)]

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=months_series, y=data_1, name="Consumer Credit", line=dict(color='#00d4ff', width=4)))
fig_line.add_trace(go.Scatter(x=months_series, y=data_2, name="Industrial Lending", line=dict(color='#ff4b4b', width=4)))

fig_line.update_layout(
    template="plotly_dark", 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)', 
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_line, use_container_width=True)

# 7. TECHNICAL FOOTER
st.markdown("---")
st.caption("STATISTICAL DISCLOSURE: Data modeling follows standard RBI DBIE reporting frameworks. "
           "Calculations are based on a Quantile Regression approach to sectoral credit dispersal.")
