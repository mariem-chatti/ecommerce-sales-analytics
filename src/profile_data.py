import pandas as pd

df = pd.read_csv("/app/data/raw/online_retail.csv")

print("DATASET SHAPE")
print(df.shape)

print("\nCOLUMN DATA TYPES")
print(df.dtypes)

print("\nMISSING VALUES")
print(df.isna().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

print("\nFIRST FIVE ROWS")
print(df.head())

print('*'*20)

#Investigate suspicious transactions
print("\nTRANSACTION QUALITY CHECKS")

print("Negative quantities:", (df["Quantity"] < 0).sum())
print("Zero quantities:", (df["Quantity"] == 0).sum())

print("Negative prices:", (df["UnitPrice"] < 0).sum())
print("Zero prices:", (df["UnitPrice"] == 0).sum())

print(
    "Cancelled invoice lines:",
    df["InvoiceNo"].astype(str).str.startswith("C").sum()
)

print("\nROWS WITH MISSING DESCRIPTIONS")
print(
    df[df["Description"].isna()]
    [["InvoiceNo", "StockCode", "Quantity", "UnitPrice"]]
    .head(10)
)
print('*'*20)
print('how many negative-quantity rows have invoice numbers that do not begin with C')
negative_qty = df["Quantity"] < 0
cancelled_invoice = df["InvoiceNo"].astype(str).str.startswith("C")

print("\nNEGATIVE QUANTITY INVESTIGATION")

print(
    "Negative quantity with C invoice:",
    (negative_qty & cancelled_invoice).sum()
)

print(
    "Negative quantity without C invoice:",
    (negative_qty & ~cancelled_invoice).sum()
)

print(
    "C invoice with non-negative quantity:",
    (~negative_qty & cancelled_invoice).sum()
)

print("\nEXAMPLES OF NEGATIVE QUANTITY WITHOUT C")
print(
    df.loc[
        negative_qty & ~cancelled_invoice,
        ["InvoiceNo", "StockCode", "Description", "Quantity", "UnitPrice"]
    ].head(10).to_string(index=False)
)
