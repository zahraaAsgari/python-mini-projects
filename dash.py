import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# Page config - Luxury & Modern Theme
st.set_page_config(
    page_title="Dubai Luxury Real Estate Dashboard - Dec 2025",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling for a premium look
st.markdown("""
    <style>
    .main {background-color: #0e1117; color: #fafafa;}
    .sidebar .sidebar-content {background-color: #1f2a44;}
    h1, h2, h3 {color: #00b7eb;}
    .metric-label {color: #a0aec0;}
    .metric-value {color: #00b7eb; font-size: 1.8rem;}
    </style>
    """, unsafe_allow_html=True)

sns.set(style="darkgrid", palette="Blues")

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("transactions-2025-12-20.csv")
    
    # Convert date
    df['INSTANCE_DATE'] = pd.to_datetime(df['INSTANCE_DATE'], errors='coerce')
    
    # Key calculated metrics (based on 2025 market insights)
    df['meter_price'] = df['TRANS_VALUE'] / df['PROCEDURE_AREA']
    df['yield_est'] = 0.065  # Average gross yield ~6.5% in 2025
    df['appreciation_est'] = 0.156  # Average capital appreciation ~15.6%
    df['roi_est'] = df['yield_est'] + df['appreciation_est'] - (20 / df['PROCEDURE_AREA']) / df['meter_price']  # Approx net ROI
    
    return df

df = load_data()

# Sidebar - Filters
st.sidebar.header("Dubai Luxury Market Filters")
st.sidebar.markdown("Explore 2025 transaction insights")

# Area filter
areas = sorted(df['AREA_EN'].dropna().unique())
selected_areas = st.sidebar.multiselect("Select Area", areas, default=areas[:5] if len(areas) > 5 else areas)

# Property type filter
prop_types = sorted(df['PROP_TYPE_EN'].dropna().unique())
selected_prop_types = st.sidebar.multiselect("Select Property Type", prop_types, default=prop_types)

# Price range
min_price, max_price = float(df['TRANS_VALUE'].min()), float(df['TRANS_VALUE'].max())
price_range = st.sidebar.slider(
    "Transaction Value Range (AED)",
    min_price, max_price,
    (min_price, max_price),
    format="%.0f"
)

# Date range
min_date = df['INSTANCE_DATE'].min().date()
max_date = df['INSTANCE_DATE'].max().date()
date_range = st.sidebar.date_input("Transaction Date Range", [min_date, max_date])

# Apply filters
filtered_df = df[
    (df['AREA_EN'].isin(selected_areas)) &
    (df['PROP_TYPE_EN'].isin(selected_prop_types)) &
    (df['TRANS_VALUE'].between(price_range[0], price_range[1])) &
    (df['INSTANCE_DATE'].dt.date >= date_range[0]) &
    (df['INSTANCE_DATE'].dt.date <= date_range[1])
]

# Main Dashboard Title
st.title("🏙️ Dubai Luxury Real Estate Dashboard - December 2025")
st.markdown("**Interactive analysis of DLD transaction data | Focus on ROI, yields, and market trends**")
st.markdown(f"**Filtered Records:** {len(filtered_df):,} | **Total Records:** {len(df):,}")

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Average Transaction Value (AED)", f"{filtered_df['TRANS_VALUE'].mean():,.0f}")
with col2:
    st.metric("Average Price per Sqm (AED)", f"{filtered_df['meter_price'].mean():,.0f}")
with col3:
    st.metric("Estimated Average ROI (%)", f"{filtered_df['roi_est'].mean() * 100:.1f}%")
with col4:
    st.metric("Total Transactions", len(filtered_df))

# Data preview (expandable)
with st.expander("View Raw Data Sample"):
    st.dataframe(filtered_df.head(10), use_container_width=True)

# Descriptive stats (expandable)
with st.expander("Descriptive Statistics"):
    st.dataframe(filtered_df.describe(), use_container_width=True)

# Visualizations Section
st.header("Market Insights & Trends")

# 1. Average Transaction Value by Area
area_avg = filtered_df.groupby('AREA_EN')['TRANS_VALUE'].mean().reset_index().sort_values('TRANS_VALUE', ascending=False)
fig1 = px.bar(
    area_avg,
    x='AREA_EN', y='TRANS_VALUE',
    color='TRANS_VALUE',
    color_continuous_scale='Blues',
    title="Average Transaction Value by Area (AED)",
    labels={'TRANS_VALUE': 'Average Value (AED)', 'AREA_EN': 'Area'}
)
fig1.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# 2. Monthly Transaction Trend
monthly_trend = filtered_df.resample('M', on='INSTANCE_DATE')['TRANS_VALUE'].mean().reset_index()
fig2 = px.line(
    monthly_trend,
    x='INSTANCE_DATE', y='TRANS_VALUE',
    markers=True,
    title="Monthly Average Transaction Value Trend (2025)",
    labels={'TRANS_VALUE': 'Average Value (AED)', 'INSTANCE_DATE': 'Date'}
)
fig2.update_traces(line=dict(color='#00b7eb', width=4))
fig2.update_layout(height=500)
st.plotly_chart(fig2, use_container_width=True)

# 3. Distribution by Property Type (Box Plot)
fig3 = px.box(
    filtered_df,
    x='PROP_TYPE_EN', y='TRANS_VALUE',
    color='PROP_TYPE_EN',
    color_discrete_sequence=px.colors.sequential.Blues_r,
    title="Transaction Value Distribution by Property Type",
    labels={'TRANS_VALUE': 'Value (AED)', 'PROP_TYPE_EN': 'Property Type'}
)
fig3.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

# 4. Correlation Heatmap
st.subheader("Feature Correlations")
numeric_cols = ['TRANS_VALUE', 'PROCEDURE_AREA', 'ACTUAL_AREA', 'meter_price', 'roi_est']
corr = filtered_df[numeric_cols].corr()
fig4, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(corr, annot=True, cmap='Blues', fmt='.2f', linewidths=0.5, ax=ax, cbar_kws={"shrink": .8})
ax.set_title("Key Variable Correlations")
st.pyplot(fig4)

# Download filtered data
st.header("Export Data")
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name=f"dubai_luxury_transactions_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("**Built with Streamlit | Data Source: Dubai Land Department (DLD) | December 2025**")
st.caption("Focus on high-ROI opportunities in Palm Jumeirah & off-plan projects for sustained growth.")