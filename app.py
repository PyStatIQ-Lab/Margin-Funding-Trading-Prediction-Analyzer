import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Margin Trading Analyzer",
    page_icon="📈",
    layout="wide"
)

# App title and description
st.title("📊 Margin Trading Portfolio Analyzer")
st.markdown("""
**Interactive dashboard for analyzing margin trading opportunities with risk metrics.**
Data is loaded from your local `margin_predictions.xlsx` file.
""")
st.markdown("---")

# Load data from Excel
try:
    df = pd.read_excel("margin_predictions.xlsx")
    
    # Display success message
    st.success("Data successfully loaded from margin_predictions.xlsx")
    
    # Show basic stats
    st.sidebar.header("Dataset Overview")
    st.sidebar.metric("Total Stocks", len(df))
    st.sidebar.metric("Avg Margin Probability", f"{df['Margin_Call_Probability'].mean():.1%}")
    st.sidebar.metric("Highest Rank", df.loc[df['Risk_Adjusted_Rank'].idxmin()]['Symbol'])
    st.sidebar.download_button("Download Current Data", df.to_csv(), "margin_data.csv", "text/csv")
    
    # Column descriptions
    st.subheader("Column Reference Guide")
    with st.expander("Click to view detailed column descriptions"):
        col_descriptions = {
            'Symbol': 'Stock ticker symbol',
            'Current_Price': 'Current market price per share (₹)',
            'Margin_Safety': 'Safety level for margin trading: Safe, Warning, or Danger',
            'Recommendation': 'Recommended action: Buy on Margin, Avoid Margin, or Hold',
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
    
    # Interactive filters
    st.subheader("Interactive Analysis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        safety_filter = st.multiselect(
            "Margin Safety",
            options=df['Margin_Safety'].unique(),
            default=df['Margin_Safety'].unique()
        )
    
    with col2:
        recommendation_filter = st.multiselect(
            "Recommendation",
            options=df['Recommendation'].unique(),
            default=df['Recommendation'].unique()
        )
    
    with col3:
        min_rank = int(df['Risk_Adjusted_Rank'].min())
        max_rank = int(df['Risk_Adjusted_Rank'].max())
        rank_filter = st.slider(
            "Risk Adjusted Rank",
            min_rank,
            max_rank,
            (min_rank, max_rank)
        )
    
    # Apply filters
    filtered_df = df[
        (df['Margin_Safety'].isin(safety_filter)) &
        (df['Recommendation'].isin(recommendation_filter)) &
        (df['Risk_Adjusted_Rank'].between(rank_filter[0], rank_filter[1]))
    ]
    
    # Show filtered stats
    st.write(f"**Displaying:** {len(filtered_df)} of {len(df)} stocks")
    
    # Interactive data table
    st.dataframe(filtered_df.style.format({
        'Current_Price': '₹{:,.2f}',
        'Predicted_Return_5d': '{:.2%}',
        'Margin_Call_Probability': '{:.1%}',
        'Value_at_Risk_95': '{:.2%}',
        'Volatility_20d': '{:.2%}',
        'Max_Position_$': '₹{:,.0f}',
        'Max_Shares': '{:,}',
        'Margin_Utilization_%': '{:.1f}%',
        'Risk_per_Share': '₹{:.2f}',
        'Fundamental_Strength': '{:.3f}',
        'Risk_Adjusted_Score': '{:.3f}'
    }).background_gradient(subset=['Risk_Adjusted_Score'], cmap='RdYlGn'), 
    height=500)
    
    # Key metrics summary
    st.subheader("Portfolio Highlights")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Top Ranked Stock", 
               filtered_df.loc[filtered_df['Risk_Adjusted_Rank'].idxmin()]['Symbol'], 
               f"Rank #{filtered_df['Risk_Adjusted_Rank'].min()}")
    
    col2.metric("Highest Potential Return", 
               filtered_df.loc[filtered_df['Predicted_Return_5d'].idxmax()]['Symbol'], 
               f"{filtered_df['Predicted_Return_5d'].max():.2%}")
    
    col3.metric("Safest Margin", 
               filtered_df.loc[filtered_df['Margin_Call_Probability'].idxmin()]['Symbol'], 
               f"{filtered_df['Margin_Call_Probability'].min():.1%} probability")
    
    col4.metric("Strong Fundamentals", 
               filtered_df.loc[filtered_df['Fundamental_Strength'].idxmax()]['Symbol'], 
               f"Score: {filtered_df['Fundamental_Strength'].max():.3f}")
    
    # Visualization
    st.markdown("---")
    st.subheader("Risk-Return Analysis")
    tab1, tab2, tab3 = st.tabs(["Risk vs Return", "Margin Safety", "Position Sizing"])
    
    with tab1:
        st.scatter_chart(
            filtered_df,
            x='Volatility_20d',
            y='Predicted_Return_5d',
            size='Max_Position_$',
            color='Risk_Adjusted_Rank'
        )
    
    with tab2:
        st.bar_chart(
            filtered_df.groupby('Margin_Safety')['Symbol'].count()
        )
    
    with tab3:
        st.bar_chart(
            filtered_df.set_index('Symbol')['Max_Position_$']
        )
    
    st.markdown("---")
    st.caption("Note: All financial values are in Indian Rupees (₹) | Data updated at: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))

except FileNotFoundError:
    st.error("⚠️ File not found. Please make sure 'margin_predictions.xlsx' is in the same directory as this app.")
    st.info("Using sample data for demonstration purposes")
    
    # Sample data
    data = {
        'Symbol': ['21STCENMGM.NS', '360ONE.NS', '3IINFOLTD.NS'],
        'Current_Price': [58.74, 1171.80, 24.49],
        'Margin_Safety': ['Safe', 'Safe', 'Safe'],
        'Recommendation': ['Buy on Margin', 'Avoid Margin', 'Buy on Margin'],
        'Predicted_Return_5d': [0.0133, -0.0004, 0.0244],
        'Margin_Call_Probability': [0.7193, 0.7385, 0.7592],
        'Value_at_Risk_95': [0.0301, 0.0401, 0.0408],
        'Volatility_20d': [0.0146, 0.0232, 0.0209],
        'Max_Position_$': [332061, 249404, 245079],
        'Max_Shares': [5653, 212, 10007],
        'Margin_Utilization_%': [66.41, 49.88, 49.02],
        'Risk_per_Share': [1.77, 46.98, 1.00],
        'Fundamental_Strength': [1.000, 0.820, 0.497],
        'Risk_Adjusted_Score': [0.442, -0.010, 0.598],
        'Risk_Adjusted_Rank': [3, 12, 2]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
