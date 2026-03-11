import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Dashboard Layout & Styling
st.set_page_config(page_title="RBI MPC Pulse", layout="wide")
st.title("MPC Pulse: Interactive Policy Simulator")
st.markdown("---")

# 2. THE SLIDER (The 'Brain' of the website)
# This is what the user will play with.
st.sidebar.header("Control Panel")
st.sidebar.write("Adjust the Repo Rate to simulate a Monetary Policy shock.")
repo_rate = st.sidebar.slider("Current Repo Rate (%)", 4.0, 10.0, 6.50, 0.25)

# We calculate 'Impact' based on our slider input
base_credit = 12.0  # Normal credit growth
# The 'Asymmetry': Hikes (above 6.5) hit harder than cuts help
if repo_rate > 6.5:
    impact = (repo_rate - 6.5) * -2.5  # Heavy hit for hikes
else:
    impact = (6.5 - repo_rate) * 1.2   # Mild boost for cuts

current_growth = base_credit + impact

# 4. BIG INTERACTIVE NUMBERS (These change when you slide!)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Simulated Repo Rate", value=f"{repo_rate}%", delta=f"{repo_rate - 6.5:.2f}%")

with col2:
    # This color changes based on the growth!
    color = "normal" if current_growth > 10 else "inverse"
    st.metric(label="Predicted Bank Credit Growth", value=f"{current_growth:.2f}%", delta=f"{impact:.2f}%", delta_color=color)

with col3:
    st.metric(label="Transmission Efficiency", value="High" if repo_rate > 6.5 else "Moderate")

# 5. THE GRAPH (That also reacts to the slider)
st.markdown("### Visualizing the Transmission")
chart_data = pd.DataFrame({
    "Sector": ["Retail Loans", "SME Loans", "Corporate Loans"],
    "Growth Rate (%)": [current_growth * 1.1, current_growth * 0.8, current_growth * 0.95]
})

fig = px.bar(chart_data, x="Sector", y="Growth Rate (%)", 
             range_y=[0, 20], color="Sector",
             title=f"Impact of {repo_rate}% Rate on Different Sectors")
st.plotly_chart(fig, use_container_width=True)

st.info(f"**Researcher's Insight:** At **{repo_rate}%**, our model shows that SMEs are the most vulnerable. I've designed this to simplify complex MPC decisions into visible risks.")

