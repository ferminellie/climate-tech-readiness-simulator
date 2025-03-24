import streamlit as st
import pandas as pd

# Title
st.title("Climate Tech Readiness Simulator")
st.markdown("Use the sliders below to simulate a company's readiness to adopt climate technologies.")

# Define input variables and weights (from weighted influence matrix)
inputs = {
    "Leadership Commitment": 5,
    "R&D Investment": 4,
    "Workforce Expertise": 4,
    "Innovation Culture": 4,
    "Digital Infrastructure": 3,
    "Internal ESG Targets": 3,
    "Policy & Regulation": 5,
    "Market Demand": 4,
    "Access to Infrastructure": 4,
    "Investor Expectations": 3,
    "Supply Chain Readiness": 3,
    "Industry Competition": 3,
    "Legacy Asset Intensity": 2
}

# Streamlit sliders
st.sidebar.header("Input Driver Scores (1–5)")
user_inputs = {}
for key in inputs:
    user_inputs[key] = st.sidebar.slider(key, 1, 5, inputs[key])

# Influence weights for each dependent outcome
influences = {
    "Climate Tech Maturity": {
        "R&D Investment": 5,
        "Workforce Expertise": 4,
        "Access to Infrastructure": 4
    },
    "Decarbonization Progress": {
        "R&D Investment": 4,
        "Internal ESG Targets": 3,
        "Policy & Regulation": 5,
        "Climate Tech Maturity": 4,
        "Sector Type": 3
    },
    "Innovation Diffusion Speed": {
        "Innovation Culture": 4,
        "Digital Infrastructure": 3,
        "Market Demand": 4,
        "Supply Chain Readiness": 3,
        "Legacy Asset Intensity": 2
    },
    "ESG Performance Trajectory": {
        "Innovation Diffusion Speed": 4,
        "Business Resilience": 3
    }
}

# Calculate readiness scores
results = {}
for outcome, drivers in influences.items():
    total_score = 0
    total_weight = 0
    for driver, weight in drivers.items():
        score = user_inputs.get(driver, 3)  # default score if missing
        total_score += score * weight
        total_weight += weight
    results[outcome] = round(total_score / total_weight, 2) if total_weight else 0

# Display output
st.header("Simulation Results")
st.write("Based on your inputs, here is how the company performs on climate tech readiness outcomes:")
st.dataframe(pd.DataFrame(results.items(), columns=["Readiness Outcome", "Score (1–5)"]))

# Radar chart (optional)
try:
    import plotly.express as px
    radar_df = pd.DataFrame(dict(
        r=list(results.values()),
        theta=list(results.keys())
    ))
    fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, title="Climate Readiness Radar Chart")
    fig.update_traces(fill='toself')
    st.plotly_chart(fig)
except:
    st.info("Plotly not available, skipping radar chart.")
