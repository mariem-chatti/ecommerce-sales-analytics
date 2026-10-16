import pandas as pd

# 1. Load the original CSV
df = pd.read_csv(
    "/app/data/raw/online_retail.csv",
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "Description": "string",
        "Country": "string",
        "CustomerID": "string"
    }
)

# Remove the unnecessary .0 suffix from CustomerID
df["CustomerID"] = df["CustomerID"].str.replace(
    r"\.0$",
    "",
    regex=True
)

# 2. Convert the invoice date
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="raise"
)

# 3. Inspect the corrected types
print("DATA TYPES AFTER CONVERSION")
print(df.dtypes)

# 4. Check that we haven't lost any records
print("\nTOTAL ROWS:", len(df))

# 5. Display a few customer IDs
print("\nCUSTOMER ID EXAMPLES")
print(df["CustomerID"].head(10))

print("\nCUSTOMER IDS AFTER CLEANING")
print(df["CustomerID"].head(10))

print("\nMISSING CUSTOMER IDS")
print(df["CustomerID"].isna().sum())

# Identify cancellation invoices
print('*'*40)

# import numpy as np

# # Identify cancellation invoices
# is_cancelled = df["InvoiceNo"].str.startswith("C").fillna(False)

# # Define transaction conditions
# conditions = [
#     is_cancelled,
#     (df["Quantity"] < 0) & ~is_cancelled,
#     (df["Quantity"] > 0) & (df["UnitPrice"] > 0),
#     (df["Quantity"] > 0) & (df["UnitPrice"] == 0)
# ]

# # Labels corresponding to the conditions
# choices = [
#     "CANCELLATION",
#     "ADJUSTMENT",
#     "SALE",
#     "ZERO_PRICE"
# ]

# df["TransactionType"] = np.select(
#     conditions,
#     choices,
#     default="REVIEW"
# )

# print("\nTRANSACTION CLASSIFICATION")
# print(df["TransactionType"].value_counts())

def classify_transaction(row):
    invoice = row["InvoiceNo"]
    quantity = row["Quantity"]
    price = row["UnitPrice"]
    description = row["Description"]
    if pd.notna(description) and description == "Adjust bad debt" and price < 0:
        return "BAD_DEBT"
    elif invoice.startswith("C"):
        return "CANCELLATION"
    elif quantity < 0:
        return "ADJUSTMENT"
    elif quantity > 0 and price > 0 : 
        return "SALE"
    elif quantity >0 and price==0 : 
        return "ZERO_PRICE"
    else: 
        return "REVIEW"
# Apply the function to every row
df["TransactionType"] = df.apply(
    classify_transaction,
    axis=1
)

print("\nTRANSACTION CLASSIFICATION")
print(df["TransactionType"].value_counts())

print('*'*40)

print("\nRECORDS REQUIRING REVIEW")

review_rows = df[df["TransactionType"] == "REVIEW"]
print(review_rows.to_string(index=False))

# Validate the cleaned dataset
print('*'*40)
assert len(df) == 541909, "Unexpected number of rows!"

assert df["InvoiceNo"].notna().all(), "Missing invoice numbers!"

assert df["InvoiceDate"].notna().all(), "Missing invoice dates!"

assert df["TransactionType"].ne("REVIEW").all(), "Unclassified transactions found!"

print("\nAll validation checks passed!")

# Save the cleaned dataset
output_file = "/app/data/processed/online_retail_cleaned.csv"

df.to_csv(output_file, index=False)

print("Cleaned dataset saved successfully!")

