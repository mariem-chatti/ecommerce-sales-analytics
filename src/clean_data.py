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

original_count = len(df)
print("ORIGINAL ROWS:", original_count)

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
print("\nCUSTOMER IDS AFTER CLEANING")
print(df["CustomerID"].head(10))

print("\nMISSING CUSTOMER IDS")
print(df["CustomerID"].isna().sum())

# 6. Remove exact duplicate rows, retaining the first occurrence.
# Assumption: identical source rows are duplicates.
duplicates_removed = int(df.duplicated().sum())

df = df.drop_duplicates().copy()

print("\nDUPLICATE REMOVAL")
print("Rows before:", original_count)
print("Rows removed:", duplicates_removed)
print("Rows after:", len(df))

# Identify cancellation invoices
print('*'*40)

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
assert original_count == 541909, "Unexpected original row count!"

assert duplicates_removed == 5268, "Unexpected duplicate count!"

assert len(df) == 536641, "Unexpected cleaned row count!"

assert not df.duplicated().any(), "Duplicates still exist!"

assert df["InvoiceNo"].notna().all(), "Missing invoice numbers!"

assert df["InvoiceDate"].notna().all(), "Missing invoice dates!"

assert df["TransactionType"].ne("REVIEW").all(), (
    "Unclassified transactions found!"
)
assert len(df) + duplicates_removed == original_count, (
    "Row count mismatch!"
)

print("\nAll validation checks passed!")

# Save the cleaned dataset
output_file = "/app/data/processed/online_retail_cleaned.csv"

df.to_csv(output_file, index=False)

print("Cleaned dataset saved successfully!")

