import pandas as pd
import numpy as np


# Step 1: Load sales data
df = pd.read_csv("sales.csv")

print("\n===== ORIGINAL DATA =====")
print(df)


# Step 2: Check missing values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


# Step 3: Clean the data
df = df.drop_duplicates()

df = df.dropna(
    subset=["Product", "Quantity", "Price"]
)

df["Product"] = df["Product"].astype(str).str.strip()

df["Quantity"] = pd.to_numeric(
    df["Quantity"],
    errors="coerce"
)

df["Price"] = pd.to_numeric(
    df["Price"],
    errors="coerce"
)

df = df.dropna(
    subset=["Quantity", "Price"]
)

df = df[
    (df["Quantity"] >= 0) &
    (df["Price"] >= 0)
].copy()


# Step 4: Calculate revenue
df["Revenue"] = df["Quantity"] * df["Price"]

print("\n===== CLEANED DATA =====")
print(df)


# Step 5: Calculate total revenue
total_revenue = df["Revenue"].sum()

print("\nTotal Revenue:", total_revenue)


# Step 6: Calculate average revenue
average_revenue = np.mean(df["Revenue"])

print("Average Product Revenue:", average_revenue)


# Step 7: Find highest revenue product
top_product = df.loc[
    df["Revenue"].idxmax()
]

print("\n===== TOP REVENUE PRODUCT =====")
print(top_product["Product"])

print("Revenue:", top_product["Revenue"])


# Step 8: Product-wise analysis
product_analysis = df.groupby("Product").agg(
    Total_Quantity=("Quantity", "sum"),
    Total_Revenue=("Revenue", "sum")
)

product_analysis = product_analysis.sort_values(
    by="Total_Revenue",
    ascending=False
)

print("\n===== PRODUCT ANALYSIS =====")
print(product_analysis)


# Step 9: Statistical analysis
print("\n===== STATISTICS =====")

print("Maximum Revenue:", np.max(df["Revenue"]))

print("Minimum Revenue:", np.min(df["Revenue"]))

print("Standard Deviation:", np.std(df["Revenue"]))


# Step 10: Export report
product_analysis.to_csv("sales_report.csv")

print("\nSales report exported successfully!")