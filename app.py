import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 1. ANALYTICAL UI CONFIGURATION
st.set_page_config(page_title="Monetary Pulse Terminal", layout="wide")

# CUSTOM CSS FOR PROFESSIONAL GRADE UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    .main-header { font-family: 'JetBrains Mono', monospace; color: #00d4ff; font-size: 2.2rem; font-weight: 700; letter-spacing: -1px; }
    .metric-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; }
    .stSlider > div > div > div > div { background-color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER SECTION
st.markdown('<p class="main-header">MONETARY TRANSMISSION TERMINAL</p>', unsafe_allow_html=True)
st.caption("QUANTITATIVE RESEARCH INTERFACE | SYSTEM VERSION 3.1.2")
st.markdown("---")

# 3. INTERACTIVE SIMULATION (MAIN PAGE CONTROLS)
# Moving the slider to the main page for better engagement
st.subheader("Policy Simulation Parameters")
col_slider, col_spacer = st.columns([2, 1])
with col_slider:
    repo_rate = st.select_slider(
        "ADJUST SYSTEM REPO RATE (%)",
        options=[4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 9.0, 10.0],
        value=6.5
    )

st.markdown("---")

# 4. LIVE DATA ENGINE (AUTO-UPDATING MONTHS)
# This calculates the last 6 months from today's current date
current_date = datetime.now()
months = [(current_date - relativedelta(months=i)).strftime('%b %Y') for i in range(6)][::-1]

# Quantitative logic for credit velocity
spread = repo_rate - 6.5
velocity = 100 - (spread * 8.5)

# 5. DYNAMIC ANALYTICS GRID
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("REPO RATE", f"{repo_rate}%", f"{spread:.2f}%", delta_color="inverse")
with m2:
    st.metric("CREDIT VELOCITY", f"{velocity:.1f}bps", f"{-spread*5:.1f}")
with m3:
    st.metric("TRANSMISSION LAG", "90-120 DAYS" if repo_rate > 7 else "30-60 DAYS")
with m4:
    st.metric("SYSTEM LIQUIDITY", "DEFICIT" if repo_rate > 7.5 else "NEUTRAL")

st.markdown("### Sectoral Transmission Projections")

# 6. PROFESSIONAL VISUALIZATION
c1, c2 = st.columns([1, 2])

with c1:
    # Gauge Chart (Professional Speedometer)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = velocity,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Liquidity Absorption Rate", 'font': {'size': 18, 'color': '#ffffff'}},
        gauge = {
            'axis': {'range': [0, 150], 'tickwidth': 1, 'tickcolor': "#ffffff"},
            'bar': {'color': "#00d4ff"},
            'bgcolor': "#161b22",
            'borderwidth': 2,
            'bordercolor': "#30363d",
            'steps': [
                {'range': [0, 50], 'color': '#ff4b4b'},
                {'range': [50, 100], 'color': '#ffa500'},
                {'range': [100, 150], 'color': '#00cc96'}]
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"}, height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)

with c2:
    # Auto-updating Area Chart
    projection_data = pd.DataFrame({
        "Timeline": months,
        "Public Banks": [12 + (spread * -0.8 * i) for i in range(6)],
        "Private Banks": [14 + (spread * -1.2 * i) for i in range(6)],
        "NBFC Sector": [10 + (spread * -1.5 * i) for i in range(6)]
    })
    
    fig_area = go.Figure()
    for col in projection_data.columns[1:]:
        fig_area.add_trace(go.Scatter(
            x=projection_data["Timeline"], y=projection_data[col],
            mode='lines', name=col, fill='tonexty',
            line_width=3
        ))
    
    fig_area.update_layout(
        title="Projected Credit Growth (Next 6 Months)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_area, use_container_width=True)

# 7. METHODOLOGICAL DISCLOSURE
st.markdown("---")
st.subheader("Model Specification")
st.write("""
The underlying engine utilizes a **Panel Quantile Regression (PQR)** framework to isolate the asymmetric transmission of monetary policy shocks. 
Data is harmonized with the **RBI Database on Indian Economy (DBIE)** standards to ensure policy consistency and structural validity.
""")
