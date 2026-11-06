
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Engineering Design Explorer",
    layout="wide"
)

st.title("Engineering Design Decision-Support Tool")

st.write(
    "Compare mechanical bracket designs using "
    "multi-attribute utility analysis."
)

st.info(
    "Demonstration only: design data and "
    "preference weights are hypothetical."
)

# Define alternatives
designs = pd.DataFrame({
    "Design": ["A", "B", "C"],
    "Cost ($)": [120, 155, 105],
    "Weight (kg)": [2.4, 1.8, 3.1],
    "Load Capacity (N)": [1800, 2200, 1600]
})

st.subheader("1. Design Alternatives")
st.dataframe(designs, hide_index=True)

# User selects importance weights
st.subheader("2. Set Attribute Importance")

cost_w = st.slider(
    "Cost importance (%)", 0, 100, 30
)

weight_w = st.slider(
    "Weight importance (%)",
    0, 100 - cost_w, min(40, 100 - cost_w)
)

load_w = 100 - cost_w - weight_w

st.write(f"Load capacity importance: {load_w}%")

# Normalize attributes
def normalize(series, higher_is_better):
    low = series.min()
    high = series.max()

    if high == low:
        return pd.Series(1.0, index=series.index)

    if higher_is_better:
        return (series - low) / (high - low)

    return (high - series) / (high - low)

results = designs.copy()

results["Cost Utility"] = normalize(
    results["Cost ($)"], False
)
results["Weight Utility"] = normalize(
    results["Weight (kg)"], False
)
results["Load Utility"] = normalize(
    results["Load Capacity (N)"], True
)

results["Overall Utility"] = (
    cost_w / 100 * results["Cost Utility"]
    + weight_w / 100 * results["Weight Utility"]
    + load_w / 100 * results["Load Utility"]
)

results = results.sort_values(
    "Overall Utility", ascending=False
)

# Display ranking
st.subheader("3. Design Ranking")

st.dataframe(
    results[["Design", "Overall Utility"]].round(4),
    hide_index=True
)

best = results.iloc[0]

st.success(
    f"Preferred Design: {best['Design']} "
    f"(Utility = {best['Overall Utility']:.4f})"
)

# Display graph
st.subheader("4. Utility Comparison")

fig, ax = plt.subplots()

ax.bar(
    results["Design"],
    results["Overall Utility"]
)

ax.set_xlabel("Design")
ax.set_ylabel("Overall Utility")
ax.set_ylim(0, 1)

st.pyplot(fig)

st.caption(
    "Ranking is based on assumed linear utility "
    "functions and user-selected weights."
)
