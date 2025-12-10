import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dubai Real Estate Dashboard", layout="wide", page_icon="🏙️")

# ---- LOAD & PREPARE DATA ----
@st.cache_data
def load_data():
    df = pd.read_csv("dubai_properties.csv")
    df.dropna(subset=["Rent", "Area_in_sqft", "Location", "Posted_date"], inplace=True)
    df["Location"] = df["Location"].str.strip().str.title()
    df["Posted_date"] = pd.to_datetime(df["Posted_date"], errors='coerce')
    df = df.dropna(subset=["Posted_date"])
    df["ROI"] = (df["Rent"] * 12 / df["Area_in_sqft"]) * 100  # Your ROI formula
    return df

df = load_data()

st.title("🏙️ Dubai Real Estate Analytics Dashboard")
st.markdown("#### Built by *AI Specialist in Progress* — Zahra")

# ---- SIDEBAR FILTERS ----
st.sidebar.header("🔍 Filters")
location_list = sorted(df["Location"].unique())
selected_locations = st.sidebar.multiselect("Select Locations", location_list, default=location_list[:10])

df_filtered = df[df["Location"].isin(selected_locations)]

# ---- KPIs ----
st.markdown("---")
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Rent (AED)", f"{int(df_filtered['Rent'].mean()):,}")
col2.metric("Avg ROI (%)", f"{df_filtered['ROI'].mean():.2f}")
col3.metric("Avg Area (sqft)", f"{int(df_filtered['Area_in_sqft'].mean()):,}")
col4.metric("Total Listings", len(df_filtered))

# ---- 1. AREA VS RENT SCATTER ----
st.markdown("---")
st.subheader("🏠 Area vs Rent")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df_filtered, x="Area_in_sqft", y="Rent", hue="Location", 
                palette="viridis", s=80, alpha=0.7, ax=ax1)
ax1.set_xlabel("Area (sqft)")
ax1.set_ylabel("Rent (AED)")
ax1.set_title("Property Size vs Rent Price", fontweight='bold')
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

# ---- 2. TOP ROI AREAS ----
st.markdown("---")
st.subheader("🏆 Top 10 ROI Locations")
roi_by_area = df_filtered.groupby("Location")["ROI"].mean().sort_values(ascending=False).head(10)
st.bar_chart(roi_by_area)

# ---- 3. TOP RENT AREAS ----
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("💰 Top 10 Expensive Locations")
    avg_rent = df_filtered.groupby("Location")["Rent"].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_rent)

with col_b:
    st.subheader("🛏️ Rent by Bedrooms")
    beds_rent = df_filtered.groupby("Beds")["Rent"].mean()
    st.bar_chart(beds_rent)

# ---- 4. MONTHLY RENT TREND ----
st.markdown("---")
st.subheader("📈 Monthly Rent Trend (Last 12 Months)")
monthly_trend = df_filtered.resample("ME", on="Posted_date")["Rent"].mean().tail(12)
fig2, ax2 = plt.subplots(figsize=(12, 6))
monthly_trend.plot(ax=ax2, linewidth=3, marker='o', color='#ff6b6b')
ax2.set_title("Rent Trend Over Time", fontweight='bold')
ax2.set_ylabel("Average Rent (AED)")
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

# ---- 5. CORRELATION HEATMAP ----
st.markdown("---")
st.subheader("🔗 Correlation Heatmap")
numeric_df = df_filtered.select_dtypes(include=['int64', 'float64'])
fig3, ax3 = plt.subplots(figsize=(12, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', linewidth=0.5, ax=ax3)
ax3.set_title('Dubai Real Estate Market Correlations', fontweight='bold')
st.pyplot(fig3)

# ---- 6. RENT DISTRIBUTION BOXPLOT ----
st.markdown("---")
st.subheader("📦 Rent Distribution by Location")
top_locations = df_filtered.groupby("Location")["Rent"].median().sort_values(ascending=False).head(15)
df_top = df_filtered[df_filtered["Location"].isin(top_locations.index)]
fig4, ax4 = plt.subplots(figsize=(15, 6))
sns.boxplot(data=df_top, x="Location", y="Rent", ax=ax4)
plt.xticks(rotation=45, ha='right')
ax4.set_title("Rent Distribution - Top Locations", fontweight='bold')
st.pyplot(fig4)

# ---- 7. ROI vs RENT SCATTER ----
st.markdown("---")
st.subheader("🎯 ROI vs Rent (Top Locations)")
top_roi_locations = df_filtered.groupby("Location")["ROI"].mean().sort_values(ascending=False).head(10)
df_top_roi = df_filtered[df_filtered["Location"].isin(top_roi_locations.index)]
fig5, ax5 = plt.subplots(figsize=(12, 6))
sns.scatterplot(data=df_top_roi, x="Rent", y="ROI", hue="Location", 
                palette="tab10", alpha=0.7, s=100, edgecolor="w", ax=ax5)
ax5.set_xlabel("Rent (AED)")
ax5.set_ylabel("ROI (%)")
ax5.set_title("ROI vs Rent - Top Performing Areas", fontweight='bold')
ax5.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
ax5.grid(True, alpha=0.3)
st.pyplot(fig5)

st.success("🚀 Dashboard Fully Loaded!")
