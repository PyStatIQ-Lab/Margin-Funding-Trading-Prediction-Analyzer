import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Margin Trading Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .header-style {
        font-size: 30px;
        font-weight: bold;
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 2px solid #1f77b4;
    }
    .card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #2ecc71;
    }
    .metric-label {
        font-size: 14px;
        color: #7f8c8d;
    }
    .top-stock-card {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white !important;
        border-radius: 10px;
        padding: 15px;
        margin: 5px 0;
    }
    .top-stock-card .symbol {
        font-weight: bold;
        font-size: 18px;
    }
    .top-stock-card .rank {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }
    .search-box {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load data function with caching
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("margin_predictions.xlsx")
        return df
    except FileNotFoundError:
        st.error("⚠️ File not found. Using sample data")
        # Sample data
        data = {
            'Symbol': ['21STCENMGM.NS', '360ONE.NS', '3IINFOLTD.NS', 'AARTIIND.NS', 'ABB.NS', 
                       'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS',
                       'ADANIPOWER.NS', 'AEGISCHEM.NS', 'AETHER.NS', 'AFFLE.NS', 'AIAENG.NS'],
            'Current_Price': [58.74, 1171.80, 24.49, 1256.50, 7820.00, 185.15, 287.40, 2670.50, 3250.75, 1385.60,
                              520.30, 725.25, 1240.80, 1580.40, 3650.25],
            'Margin_Safety': ['Safe', 'Safe', 'Safe', 'Warning', 'Safe', 'Danger', 'Safe', 'Warning', 'Safe', 'Safe',
                              'Warning', 'Danger', 'Safe', 'Safe', 'Warning'],
            'Recommendation': ['Buy on Margin', 'Avoid Margin', 'Buy on Margin', 'Hold', 'Buy on Margin', 
                              'Avoid Margin', 'Hold', 'Buy on Margin', 'Avoid Margin', 'Buy on Margin',
                              'Hold', 'Avoid Margin', 'Buy on Margin', 'Hold', 'Buy on Margin'],
            'Predicted_Return_5d': [0.0133, -0.0004, 0.0244, 0.0085, 0.0152, -0.0125, 0.0055, 0.0098, -0.0072, 0.0115,
                                    -0.0035, -0.0155, 0.0185, 0.0065, 0.0128],
            'Margin_Call_Probability': [0.7193, 0.7385, 0.7592, 0.6825, 0.5987, 0.8525, 0.6325, 0.7125, 0.7652, 0.6925,
                                        0.8025, 0.8750, 0.6250, 0.6550, 0.7025],
            'Value_at_Risk_95': [0.0301, 0.0401, 0.0408, 0.0352, 0.0285, 0.0455, 0.0325, 0.0382, 0.0425, 0.0365,
                                 0.0415, 0.0485, 0.0295, 0.0315, 0.0375],
            'Volatility_20d': [0.0146, 0.0232, 0.0209, 0.0185, 0.0162, 0.0255, 0.0175, 0.0195, 0.0225, 0.0185,
                               0.0215, 0.0265, 0.0155, 0.0165, 0.0195],
            'Max_Position_$': [332061, 249404, 245079, 185245, 425698, 98562, 156325, 298745, 325698, 412365,
                               187542, 89562, 265874, 198745, 356987],
            'Max_Shares': [5653, 212, 10007, 147, 54, 532, 544, 112, 100, 297,
                           360, 123, 214, 126, 98],
            'Margin_Utilization_%': [66.41, 49.88, 49.02, 72.85, 58.74, 85.25, 63.25, 71.25, 76.52, 69.25,
                                     80.25, 87.50, 62.50, 65.50, 70.25],
            'Risk_per_Share': [1.77, 46.98, 1.00, 8.52, 142.25, 3.48, 5.28, 23.85, 32.50, 12.45,
                               14.25, 7.25, 18.50, 12.55, 37.25],
            'Fundamental_Strength': [1.000, 0.820, 0.497, 0.745, 0.895, 0.325, 0.685, 0.825, 0.925, 0.875,
                                     0.745, 0.425, 0.865, 0.755, 0.895],
            'Risk_Adjusted_Score': [0.442, -0.010, 0.598, 0.325, 0.685, -0.125, 0.285, 0.412, -0.085, 0.365,
                                    -0.125, -0.225, 0.525, 0.325, 0.425],
            'Risk_Adjusted_Rank': [3, 12, 2, 8, 4, 15, 10, 7, 13, 6, 14, 16, 1, 9, 5]
        }
        return pd.DataFrame(data)

# Load data
df = load_data()

# Sort by rank for top performers
top_10 = df.sort_values('Risk_Adjusted_Rank').head(10).reset_index(drop=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/477/477103.png", width=80)
    st.title("Margin Trading Analyzer")
    st.markdown("---")
    
    st.subheader("Overall Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Total Stocks", len(df))
    col2.metric("Avg Risk Score", f"{df['Risk_Adjusted_Score'].mean():.3f}")
    
    st.markdown("---")
    st.subheader("Filters")
    
    # Margin Safety filter
    safety_options = st.multiselect(
        "Margin Safety",
        options=df['Margin_Safety'].unique(),
        default=df['Margin_Safety'].unique()
    )
    
    # Recommendation filter
    recommendation_options = st.multiselect(
        "Recommendation",
        options=df['Recommendation'].unique(),
        default=df['Recommendation'].unique()
    )
    
    # Risk Rank range
    min_rank = int(df['Risk_Adjusted_Rank'].min())
    max_rank = int(df['Risk_Adjusted_Rank'].max())
    rank_range = st.slider(
        "Risk Adjusted Rank Range",
        min_rank, max_rank, (min_rank, 10)
    )
    
    # Price range
    min_price = df['Current_Price'].min()
    max_price = df['Current_Price'].max()
    price_range = st.slider(
        "Price Range (₹)",
        min_price, max_price, (min_price, max_price)
    )
    
    st.markdown("---")
    st.caption("Data updated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))

# Apply filters
filtered_df = df[
    (df['Margin_Safety'].isin(safety_options)) &
    (df['Recommendation'].isin(recommendation_options)) &
    (df['Risk_Adjusted_Rank'].between(rank_range[0], rank_range[1])) &
    (df['Current_Price'].between(price_range[0], price_range[1]))
]

# Main dashboard
st.markdown('<p class="header-style">Margin Trading Portfolio Dashboard</p>', unsafe_allow_html=True)

# Top metrics row
st.subheader("Portfolio Summary")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card"><div class="metric-label">Top Ranked Stock</div>'
                f'<div class="metric-value">{top_10.loc[0, "Symbol"]}</div>'
                f'<div>Rank #1 | Score: {top_10.loc[0, "Risk_Adjusted_Score"]:.3f}</div></div>', 
                unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="metric-label">Highest Potential Return</div>'
                f'<div class="metric-value">{filtered_df.loc[filtered_df["Predicted_Return_5d"].idxmax(), "Symbol"]}</div>'
                f'<div>{filtered_df["Predicted_Return_5d"].max():.2%} | ₹{filtered_df.loc[filtered_df["Predicted_Return_5d"].idxmax(), "Current_Price"]:,.2f}</div></div>', 
                unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card"><div class="metric-label">Lowest Risk/Share</div>'
                f'<div class="metric-value">{filtered_df.loc[filtered_df["Risk_per_Share"].idxmin(), "Symbol"]}</div>'
                f'<div>₹{filtered_df["Risk_per_Share"].min():.2f} | {filtered_df.loc[filtered_df["Risk_per_Share"].idxmin(), "Margin_Safety"]} Margin</div></div>', 
                unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card"><div class="metric-label">Strong Fundamentals</div>'
                f'<div class="metric-value">{filtered_df.loc[filtered_df["Fundamental_Strength"].idxmax(), "Symbol"]}</div>'
                f'<div>Score: {filtered_df["Fundamental_Strength"].max():.3f} | ₹{filtered_df.loc[filtered_df["Fundamental_Strength"].idxmax(), "Current_Price"]:,.2f}</div></div>', 
                unsafe_allow_html=True)

# Top 10 Stocks Section
st.subheader("Top 10 Ranked Stocks")
cols = st.columns(5)
for i, row in top_10.head(5).iterrows():
    with cols[i % 5]:
        st.markdown(f'''
        <div class="top-stock-card">
            <div class="rank">#{i+1}</div>
            <div class="symbol">{row['Symbol']}</div>
            <div>Price: ₹{row['Current_Price']:,.2f}</div>
            <div>Return: {row['Predicted_Return_5d']:.2%}</div>
            <div>Risk: {row['Risk_per_Share']:.2f}</div>
        </div>
        ''', unsafe_allow_html=True)

if len(top_10) > 5:
    cols = st.columns(5)
    for i, row in top_10[5:10].iterrows():
        with cols[i % 5]:
            st.markdown(f'''
            <div class="top-stock-card">
                <div class="rank">#{i+1}</div>
                <div class="symbol">{row['Symbol']}</div>
                <div>Price: ₹{row['Current_Price']:,.2f}</div>
                <div>Return: {row['Predicted_Return_5d']:.2%}</div>
                <div>Risk: {row['Risk_per_Share']:.2f}</div>
            </div>
            ''', unsafe_allow_html=True)

# Stock Search Section
st.subheader("Stock Search & Analysis")
with st.container():
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    
    # Search input
    search_term = st.text_input("Search by stock symbol:", placeholder="Enter stock symbol...")
    
    if search_term:
        search_results = df[df['Symbol'].str.contains(search_term, case=False)]
    else:
        search_results = filtered_df
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display search results
    if not search_results.empty:
        # Format the dataframe
        formatted_df = search_results.copy()
        formatting = {
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
        }
        
        for col, fmt in formatting.items():
            formatted_df[col] = formatted_df[col].apply(lambda x: fmt.format(x))
        
        # Display in an interactive table
        st.dataframe(formatted_df, height=min(400, 35 * len(search_results) + 35)
        
        # Detailed view for selected stock
        if len(search_results) == 1:
            selected = search_results.iloc[0]
            st.subheader(f"Detailed Analysis: {selected['Symbol']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Price & Fundamentals**")
                st.metric("Current Price", f"₹{selected['Current_Price']:,.2f}")
                st.metric("Fundamental Strength", f"{selected['Fundamental_Strength']:.3f}")
                st.metric("Volatility (20d)", f"{selected['Volatility_20d']:.2%}")
                
            with col2:
                st.markdown("**Risk Metrics**")
                st.metric("Margin Call Probability", f"{selected['Margin_Call_Probability']:.1%}")
                st.metric("Value at Risk (95%)", f"{selected['Value_at_Risk_95']:.2%}")
                st.metric("Risk per Share", f"₹{selected['Risk_per_Share']:.2f}")
                
            with col3:
                st.markdown("**Position Sizing**")
                st.metric("Max Position", f"₹{selected['Max_Position_$']:,.0f}")
                st.metric("Max Shares", f"{selected['Max_Shares']:,}")
                st.metric("Margin Utilization", f"{selected['Margin_Utilization_%']:.1f}%")
                
            # Create a radar chart for risk profile
            radar_df = pd.DataFrame(dict(
                r=[
                    selected['Predicted_Return_5d'] * 100,  # Scale for visibility
                    1 - selected['Risk_per_Share']/100,
                    1 - selected['Volatility_20d'],
                    1 - selected['Value_at_Risk_95'],
                    1 - selected['Margin_Call_Probability']
                ],
                theta=['Return', 'Risk/Share', 'Volatility', 'VaR', 'Margin Probability']
            ))
            
            fig = px.line_polar(
                radar_df, 
                r='r', 
                theta='theta', 
                line_close=True,
                title=f"Risk Profile: {selected['Symbol']}",
                height=300
            )
            fig.update_traces(fill='toself')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No stocks found matching your search criteria")

# Column reference
with st.expander("Column Descriptions Reference"):
    col_descriptions = {
        'Symbol': 'Stock ticker symbol',
        'Current_Price': 'Current market price per share (₹)',
        'Margin_Safety': 'Safety level for margin trading: Safe, Warning, or Danger',
        'Recommendation': 'Recommended action: Buy on Margin, Avoid Margin, or Hold',
        'Predicted_Return_5d': 'Expected return over next 5 trading days',
        'Margin_Call_Probability': 'Probability of facing a margin call (0-1 scale)',
        'Value_at_Risk_95': 'Maximum potential loss with 95% confidence',
        'Volatility_20d': '20-day historical volatility measure',
        'Max_Position_$': 'Maximum recommended investment amount (₹)',
        'Max_Shares': 'Maximum shares to buy within risk limits',
        'Margin_Utilization_%': 'Percentage of available margin currently used',
        'Risk_per_Share': 'Estimated risk amount per share (₹)',
        'Fundamental_Strength': 'Fundamental health score (0-1, 1=strongest)',
        'Risk_Adjusted_Score': 'Performance score accounting for risk (higher=better)',
        'Risk_Adjusted_Rank': 'Rank among peers based on risk-adjusted performance (lower=better)'
    }
    
    for col, desc in col_descriptions.items():
        st.markdown(f"**{col}**: {desc}")

# Footer
st.markdown("---")
st.caption("© 2023 Margin Trading Analyzer | Data updates automatically from margin_predictions.xlsx")
