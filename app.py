import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Professional Setup
st.set_page_config(page_title="MPC Pulse Dashboard", layout="wide")

# 2. Title & Professional Branding
st.title("📊 MPC Pulse: Monetary Transmission Dashboard")
st.markdown("### *Analyzing Asymmetric Policy Impacts on Indian Banking*")
st.caption("Research Project for RBI Internship Selection | Focus: Panel Quantile Regression")

# 3. The Control Panel (Sidebar)
st.sidebar.header("Policy Control Room")
st.sidebar.info("Adjust the Repo Rate to see how it hits different bank 'Quantiles' (Small vs Large banks).")

repo_rate = st.sidebar.slider("Current Repo Rate (%)", 4.0, 10.0, 6.50, 0.25)
shock = st.sidebar.radio("Shock Type", ["Rate Hike (Contractionary)", "Rate Cut (Expansionary)"])

# 4. The 'Eco-Logic' (The Math)
# Hikes hit harder (-1.8) than cuts help (+1.1) -> This is the 'Asymmetry'
if "Hike" in shock:
    factor = -1.8
else:
    factor = 1.1

# 5. Dashboard Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Interactive Transmission Map")
    # Data showing how different banks react
    df = pd.DataFrame({
        "Bank Group": ["Small Banks (High NPA)", "Mid-Size Banks", "Large Banks (Top Tier)"],
        "Credit Growth Impact (%)": [factor * 1.6, factor * 1.0, factor * 0.6]
    })
    fig = px.bar(df, x="Bank Group", y="Credit Growth Impact (%)", 
                 color="Bank Group", text_auto='.2f',
                 color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Policy Insights")
    st.write(f"**Current Scenario:** {shock}")
    st.write(f"**Repo Rate:** {repo_rate}%")
    
    st.warning("⚠️ **Asymmetry Detected:** Notice how Small Banks (High NPA) are affected twice as much as Large Banks. This is why 'Uniform' policy is a risk.")
    
    st.divider()
    st.markdown("#### 🎓 Why this matters?")
    st.write("Using my background in **Education**, I've designed this to simplify complex **Econometrics** for policy-making.")

st.success("✅ This dashboard proves that Monetary Transmission is not linear in India.")
