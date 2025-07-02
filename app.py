import streamlit as st
import pandas as pd

# Sample data
data = {
    'Symbol': ['21STCENMGM.NS', '360ONE.NS', '3IINFOLTD.NS'],
    'Current_Price': [58.74000168, 1171.800049, 24.48999977],
    'Margin_Safety': ['Safe', 'Safe', 'Safe'],
    'Recommendation': ['Buy on Margin', 'Avoid Margin', 'Buy on Margin'],
    'Predicted_Return_5d': [0.013321424, -0.000390915, 0.024416649],
    'Margin_Call_Probability': [0.719333123, 0.738503651, 0.759175215],
    'Value_at_Risk_95': [0.030114936, 0.040095611, 0.040803189],
    'Volatility_20d': [0.014600857, 0.023221702, 0.020885948],
    'Max_Position_$': [332061.1457, 249403.8553, 245078.8819],
    'Max_Shares': [5653, 212, 10007],
    'Margin_Utilization_%': [66.41222915, 49.88077106, 49.01577638],
    'Risk_per_Share': [1.768951364, 46.98403909, 0.999270096],
    'Fundamental_Strength': [1, 0.81975, 0.49675],
    'Risk_Adjusted_Score': [0.442352722, -0.009749581, 0.598400507],
    'Risk_Adjusted_Rank': [3, 12, 2]
}

df = pd.DataFrame(data)

# App title
st.title('Stock Portfolio Analysis Dashboard')
st.markdown("---")

# Column descriptions
st.subheader("Column Descriptions")
with st.expander("Click to view column explanations"):
    col_descriptions = {
        'Symbol': 'Stock ticker symbol',
        'Current_Price': 'Current market price per share (₹)',
        'Margin_Safety': 'Safety level for margin trading (Safe/Warning/Danger)',
        'Recommendation': 'Trading recommendation based on analysis',
        'Predicted_Return_5d': 'Expected return over next 5 trading days (decimal)',
        'Margin_Call_Probability': 'Probability of facing a margin call (0-1 scale)',
        'Value_at_Risk_95': 'Maximum potential loss with 95% confidence (decimal)',
        'Volatility_20d': '20-day historical volatility measure (standard deviation)',
        'Max_Position_$': 'Maximum recommended investment amount (₹)',
        'Max_Shares': 'Maximum shares to buy within risk limits',
        'Margin_Utilization_%': 'Percentage of available margin currently used',
        'Risk_per_Share': 'Estimated risk amount per share (₹)',
        'Fundamental_Strength': 'Fundamental health score (0-1, 1=strongest)',
        'Risk_Adjusted_Score': 'Performance score accounting for risk (higher=better)',
        'Risk_Adjusted_Rank': 'Rank among peers based on risk-adjusted performance'
    }
    
    for col, desc in col_descriptions.items():
        st.markdown(f"**{col}**: {desc}")

# Interactive data table
st.subheader("Stock Analysis Data")
st.dataframe(df.style.format({
    'Current_Price': '{:.2f}',
    'Predicted_Return_5d': '{:.2%}',
    'Margin_Call_Probability': '{:.1%}',
    'Value_at_Risk_95': '{:.2%}',
    'Volatility_20d': '{:.2%}',
    'Max_Position_$': '₹{:,.0f}',
    'Margin_Utilization_%': '{:.1f}%',
    'Risk_per_Share': '{:.2f}',
    'Fundamental_Strength': '{:.3f}',
    'Risk_Adjusted_Score': '{:.3f}'
}))

# Key metrics summary
st.subheader("Key Metrics Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Highest Rank", df.loc[df['Risk_Adjusted_Rank'].idxmin()]['Symbol'], f"Rank {df['Risk_Adjusted_Rank'].min()}")
col2.metric("Lowest Risk/Share", df.loc[df['Risk_per_Share'].idxmin()]['Symbol'], f"₹{df['Risk_per_Share'].min():.2f}")
col3.metric("Highest Predicted Return", df.loc[df['Predicted_Return_5d'].idxmax()]['Symbol'], f"{df['Predicted_Return_5d'].max():.2%}")

st.markdown("---")
st.caption("Note: All financial values are in Indian Rupees (₹)")
