import pandas as pd

df = pd.read_csv(
    "/app/data/processed/online_retail_cleaned.csv",
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    }
)

print("Maximum text lengths:")
for col in ["InvoiceNo", "StockCode", "Description",
            "CustomerID", "Country", "TransactionType"]:
    print(f"{col}: {df[col].str.len().max()}")

print("\nQuantity range:")
print("Minimum:", df["Quantity"].min())
print("Maximum:", df["Quantity"].max())

print("\nUnitPrice range:")
print("Minimum:", df["UnitPrice"].min())
print("Maximum:", df["UnitPrice"].max())

print("\nPrices with more than 2 decimal places:")
extra_decimals = (
    (df["UnitPrice"] - df["UnitPrice"].round(2)).abs() > 1e-9
)

print(extra_decimals.sum())
print(
    df.loc[extra_decimals, "UnitPrice"]
      .drop_duplicates()
      .head(10)
      .to_string(index=False)
)