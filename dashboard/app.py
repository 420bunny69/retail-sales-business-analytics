
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Retail Business Analytics",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# LOAD DATA
# -------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        BASE_DIR / "data" / "Sample - Superstore.csv",
        encoding="latin1"
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"], format="%m/%d/%Y"
    )

    df["Profit Margin"] = (
        df["Profit"] / df["Sales"] * 100
    )

    df["Year-Month"] = (
        df["Order Date"].dt.to_period("M").astype(str)
    )

    return df


df = load_data()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------

st.sidebar.title("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(
        df["Order Date"].min().date(),
        df["Order Date"].max().date()
    )
)

filtered = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
].copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered = filtered[
        (filtered["Order Date"].dt.date >= start_date) &
        (filtered["Order Date"].dt.date <= end_date)
    ]

# -------------------------------
# DASHBOARD HEADER
# -------------------------------

st.title("Retail Sales & Business Analytics")
st.caption(
    "Interactive analysis of retail sales, "
    "profitability and business performance"
)

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# -------------------------------
# KEY PERFORMANCE INDICATORS
# -------------------------------

revenue = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order ID"].nunique()
customers = filtered["Customer ID"].nunique()

margin = profit / revenue * 100 if revenue else 0

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Revenue", f"${revenue:,.0f}")
c2.metric("Total Profit", f"${profit:,.0f}")
c3.metric("Profit Margin", f"{margin:.2f}%")
c4.metric("Total Orders", f"{orders:,}")
c5.metric("Customers", f"{customers:,}")

st.divider()

# -------------------------------
# MONTHLY SALES & PROFIT TRENDS
# -------------------------------

st.subheader("Sales & Profit Trends")

monthly = filtered.groupby("Year-Month").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

trend_col1, trend_col2 = st.columns(2)

with trend_col1:
    fig_revenue = px.line(
        monthly,
        x="Year-Month",
        y="Sales",
        markers=True,
        title="Monthly Revenue"
    )
    fig_revenue.update_traces(
        line=dict(color="#29b6f6", width=2.5),
        marker=dict(size=6, color="#0288d1"),
        hovertemplate="<b>Month:</b> %{x}<br><b>Revenue:</b> $%{y:,.2f}<extra></extra>"
    )
    fig_revenue.update_layout(
        xaxis_title="Year-Month",
        yaxis_title="Revenue ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        hovermode="x unified"
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

with trend_col2:
    fig_profit = px.line(
        monthly,
        x="Year-Month",
        y="Profit",
        markers=True,
        title="Monthly Profit"
    )
    fig_profit.add_hline(
        y=0,
        line_dash="dash",
        line_color="#ef5350",
        annotation_text="Break-even ($0)",
        annotation_position="bottom right"
    )
    fig_profit.update_traces(
        line=dict(color="#66bb6a", width=2.5),
        marker=dict(
            size=6,
            color=["#26a69a" if val >= 0 else "#ef5350" for val in monthly["Profit"]]
        ),
        hovertemplate="<b>Month:</b> %{x}<br><b>Profit:</b> $%{y:,.2f}<extra></extra>"
    )
    fig_profit.update_layout(
        xaxis_title="Year-Month",
        yaxis_title="Profit ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        hovermode="x unified"
    )
    st.plotly_chart(fig_profit, use_container_width=True)

# -------------------------------
# CATEGORY & REGION ANALYSIS
# -------------------------------

left, right = st.columns(2)

with left:
    st.subheader("Category Performance")

    category = filtered.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()

    fig_category = px.bar(
        category,
        x="Category",
        y="Sales",
        color="Profit",
        title="Revenue by Category",
        color_continuous_scale="RdYlGn"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with right:
    st.subheader("Regional Performance")

    region = filtered.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()

    fig_region = px.bar(
        region,
        x="Region",
        y="Profit",
        color="Region",
        title="Profit by Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

# -------------------------------
# PRODUCT PROFITABILITY
# -------------------------------

st.subheader("Sub-Category Profitability")

subcat = filtered.groupby("Sub-Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

fig_subcat = px.bar(
    subcat.sort_values("Profit"),
    x="Profit",
    y="Sub-Category",
    orientation="h",
    color="Profit",
    title="Profit and Loss by Sub-Category",
    color_continuous_scale="RdYlGn"
)

st.plotly_chart(
    fig_subcat,
    use_container_width=True
)

# -------------------------------
# DISCOUNT ANALYSIS
# -------------------------------

st.subheader("Discount Impact on Profitability")

discount = filtered.groupby("Discount").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Records=("Profit", "count")
).reset_index()

fig_discount = px.bar(
    discount,
    x="Discount",
    y="Profit",
    color="Profit",
    title="Profit by Discount Level",
    color_continuous_scale="RdYlGn"
)

st.plotly_chart(
    fig_discount,
    use_container_width=True
)

# -------------------------------
# LOSS-MAKING PRODUCTS
# -------------------------------

st.subheader("Top 10 Loss-Making Products")

products = filtered.groupby("Product Name").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()

loss_products = (
    products[products["Profit"] < 0]
    .sort_values("Profit")
    .head(10)
)

st.dataframe(
    loss_products.style.format({
        "Revenue": "${:,.2f}",
        "Profit": "${:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

# -------------------------------
# BUSINESS SUMMARY
# -------------------------------

st.divider()

st.subheader("Business Performance Summary")

st.write(
    f"""
    - Total revenue generated: **${revenue:,.2f}**
    - Total profit generated: **${profit:,.2f}**
    - Overall profit margin: **{margin:.2f}%**
    - Number of unique orders: **{orders:,}**
    - Number of unique customers: **{customers:,}**
    """
)

# -------------------------------
# KEY BUSINESS INSIGHTS
# -------------------------------

st.divider()
st.subheader("Key Business Insights")

# 1 & 2. Category Performance Insights
cat_summary = filtered.groupby("Category").agg(
    Total_Profit=("Profit", "sum")
).reset_index()

# 3 & 4. Regional Performance Insights
reg_summary = filtered.groupby("Region").agg(
    Total_Profit=("Profit", "sum")
).reset_index()

# 5. Discount Analysis for Warning
disc_summary = filtered.groupby("Discount").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).reset_index()

disc_summary["Profit_Margin"] = disc_summary.apply(
    lambda r: (r["Total_Profit"] / r["Total_Sales"] * 100) if r["Total_Sales"] != 0 else 0.0,
    axis=1
)

insight_c1, insight_c2, insight_c3, insight_c4 = st.columns(4)

with insight_c1:
    if not cat_summary.empty:
        most_prof_cat = cat_summary.loc[cat_summary["Total_Profit"].idxmax()]
        p_val = most_prof_cat["Total_Profit"]
        st.metric(
            label="Most Profitable Category",
            value=f"${p_val:,.0f}" if p_val >= 0 else f"-${abs(p_val):,.0f}",
            delta=str(most_prof_cat["Category"]),
            delta_color="normal"
        )
    else:
        st.metric("Most Profitable Category", "N/A")

with insight_c2:
    if not cat_summary.empty:
        least_prof_cat = cat_summary.loc[cat_summary["Total_Profit"].idxmin()]
        p_val = least_prof_cat["Total_Profit"]
        st.metric(
            label="Least Profitable Category",
            value=f"${p_val:,.0f}" if p_val >= 0 else f"-${abs(p_val):,.0f}",
            delta=str(least_prof_cat["Category"]),
            delta_color="inverse" if p_val < 0 else "off"
        )
    else:
        st.metric("Least Profitable Category", "N/A")

with insight_c3:
    if not reg_summary.empty:
        best_prof_reg = reg_summary.loc[reg_summary["Total_Profit"].idxmax()]
        p_val = best_prof_reg["Total_Profit"]
        st.metric(
            label="Best Performing Region",
            value=f"${p_val:,.0f}" if p_val >= 0 else f"-${abs(p_val):,.0f}",
            delta=str(best_prof_reg["Region"]),
            delta_color="normal"
        )
    else:
        st.metric("Best Performing Region", "N/A")

with insight_c4:
    if not reg_summary.empty:
        lowest_prof_reg = reg_summary.loc[reg_summary["Total_Profit"].idxmin()]
        p_val = lowest_prof_reg["Total_Profit"]
        st.metric(
            label="Lowest Performing Region",
            value=f"${p_val:,.0f}" if p_val >= 0 else f"-${abs(p_val):,.0f}",
            delta=str(lowest_prof_reg["Region"]),
            delta_color="inverse" if p_val < 0 else "off"
        )
    else:
        st.metric("Lowest Performing Region", "N/A")

# Detailed explanation cards for Category & Regional findings
with st.container():
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        if not cat_summary.empty:
            cat_least_val = least_prof_cat["Total_Profit"]
            status_text = (
                f"operating at a net loss of **-${abs(cat_least_val):,.2f}**"
                if cat_least_val < 0
                else f"delivering the lowest net profit of **${cat_least_val:,.2f}**"
            )
            st.info(
                f"**Category Profitability Breakdown:**\n\n"
                f"- **{most_prof_cat['Category']}** leads overall profitability with **${most_prof_cat['Total_Profit']:,.2f}** in total profit.\n"
                f"- **{least_prof_cat['Category']}** is the lowest contributor, {status_text}."
            )
    with info_col2:
        if not reg_summary.empty:
            reg_lowest_val = lowest_prof_reg["Total_Profit"]
            reg_status_text = (
                f"operating at a net loss of **-${abs(reg_lowest_val):,.2f}**"
                if reg_lowest_val < 0
                else f"delivering the lowest net profit of **${reg_lowest_val:,.2f}**"
            )
            st.info(
                f"**Regional Profitability Breakdown:**\n\n"
                f"- **{best_prof_reg['Region']}** is the top-performing region, generating **${best_prof_reg['Total_Profit']:,.2f}** in total profit.\n"
                f"- **{lowest_prof_reg['Region']}** is the lowest-performing region, {reg_status_text}."
            )

# Discount Warning
if not disc_summary.empty:
    lowest_margin_row = disc_summary.loc[disc_summary["Profit_Margin"].idxmin()]
    disc_rate = lowest_margin_row["Discount"]
    disc_margin = lowest_margin_row["Profit_Margin"]
    disc_profit = lowest_margin_row["Total_Profit"]
    disc_sales = lowest_margin_row["Total_Sales"]

    profit_desc = f"-${abs(disc_profit):,.2f} (net loss)" if disc_profit < 0 else f"${disc_profit:,.2f}"

    st.warning(
        f"⚠️ **Discount Warning — Profitability Exposure:**\n\n"
        f"An observed association indicates that transactions at a **{disc_rate:.0%}** discount level "
        f"yield the lowest profit margin (**{disc_margin:.2f}%**), "
        f"generating {profit_desc} on **${disc_sales:,.2f}** in sales. "
        f"Review pricing and discount strategies at this tier to mitigate margin dilution."
    )

st.caption("Retail Sales Analytics | Python, SQL & Streamlit")
