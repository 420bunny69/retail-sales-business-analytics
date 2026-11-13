
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Sample - Superstore.csv"
VISUALS_DIR = BASE_DIR / "visuals"

VISUALS_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH, encoding="latin1")

# -------------------------------
# 1. DATA CLEANING
# -------------------------------

df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="%m/%d/%Y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], format="%m/%d/%Y"
)

print("\n========== DATA QUALITY ==========")

print("Original records:", len(df))
print("Duplicate rows:", df.duplicated().sum())
print("Missing values:", df.isnull().sum().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Create additional analytical columns
df["Profit Margin"] = df["Profit"] / df["Sales"] * 100
df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)

# -------------------------------
# 2. BUSINESS KPIs
# -------------------------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
profit_margin = (total_profit / total_sales) * 100

print("\n========== BUSINESS KPIs ==========")
print(f"Total Revenue: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Overall Profit Margin: {profit_margin:.2f}%")

# -------------------------------
# 3. CATEGORY ANALYSIS
# -------------------------------

print("\n========== CATEGORY PERFORMANCE ==========")

category_analysis = df.groupby("Category").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Quantity=("Quantity", "sum")
)

category_analysis["Profit Margin %"] = (
    category_analysis["Profit"] /
    category_analysis["Sales"] * 100
)

print(category_analysis.sort_values("Sales", ascending=False))

# -------------------------------
# 4. REGIONAL ANALYSIS
# -------------------------------

print("\n========== REGIONAL PERFORMANCE ==========")

region_analysis = df.groupby("Region").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)

region_analysis["Profit Margin %"] = (
    region_analysis["Profit"] /
    region_analysis["Sales"] * 100
)

print(region_analysis.sort_values("Sales", ascending=False))

# -------------------------------
# 5. LOSS-MAKING PRODUCTS
# -------------------------------

print("\n========== TOP 10 LOSS-MAKING PRODUCTS ==========")

product_analysis = df.groupby("Product Name").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)

loss_products = product_analysis[
    product_analysis["Profit"] < 0
].sort_values("Profit").head(10)

print(loss_products)

# -------------------------------
# 6. DISCOUNT ANALYSIS
# -------------------------------

print("\n========== DISCOUNT ANALYSIS ==========")

discount_analysis = df.groupby("Discount").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)

discount_analysis["Profit Margin %"] = (
    discount_analysis["Profit"] /
    discount_analysis["Sales"] * 100
)

print(discount_analysis)

# -------------------------------
# 7. MONTHLY SALES TREND
# -------------------------------

monthly_sales = df.groupby("Year-Month").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)

# -------------------------------
# 8. VISUALIZATIONS
# -------------------------------

# Chart 1: Category Sales
category_analysis["Sales"].plot(
    kind="bar", title="Sales by Category"
)
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig(VISUALS_DIR / "category_sales.png")
plt.close()

# Chart 2: Regional Profit
region_analysis["Profit"].plot(
    kind="bar", title="Profit by Region"
)
plt.ylabel("Profit ($)")
plt.tight_layout()
plt.savefig(VISUALS_DIR / "regional_profit.png")
plt.close()

# Chart 3: Monthly Sales Trend
monthly_sales["Sales"].plot(
    figsize=(12, 5),
    title="Monthly Sales Trend"
)
plt.ylabel("Sales ($)")
plt.xlabel("Year-Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(VISUALS_DIR / "monthly_sales.png")
plt.close()

print("\nAnalysis completed successfully!")
print("Charts saved in:", VISUALS_DIR)
