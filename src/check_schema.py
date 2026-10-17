import pandas as pd

df = pd.read_csv(
    "/app/data/processed/online_retail_cleaned.csv",
    dtype={
        "CustomerID": "string",
        "StockCode": "string"
    }
)

# How many customers appear in multiple countries?
customer_countries = (
    df.dropna(subset=["CustomerID"])
      .groupby("CustomerID")["Country"]
      .nunique()
)

print(
    "Customers with multiple countries:",
    (customer_countries > 1).sum()
)

# How many product codes have multiple descriptions?
product_descriptions = (
    df.groupby("StockCode")["Description"]
      .nunique()
)

print(
    "Products with multiple descriptions:",
    (product_descriptions > 1).sum()
)

# How many transactions have unknown customers?
print(
    "Transactions with unknown customers:",
    df["CustomerID"].isna().sum()
)

print("\nCUSTOMERS WITH MULTIPLE COUNTRIES")

problem_customers = customer_countries[
    customer_countries > 1
].index

print(
    df.loc[
        df["CustomerID"].isin(problem_customers),
        ["CustomerID", "Country"]
    ]
    .drop_duplicates()
    .sort_values(["CustomerID", "Country"])
    .to_string(index=False)
)

print("\nPRODUCTS WITH MULTIPLE DESCRIPTIONS")

problem_products = product_descriptions[
    product_descriptions > 1
].index

print(
    df.loc[
        df["StockCode"].isin(problem_products),
        ["StockCode", "Description"]
    ]
    .drop_duplicates()
    .sort_values(["StockCode", "Description"])
    .head(30)
    .to_string(index=False)
)