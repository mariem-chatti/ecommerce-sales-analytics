import pandas as pd

# Location of the original Excel file inside Docker
input_file = "/app/data/raw/Online Retail.xlsx"

# Location where we want to save the CSV file
output_file = "/app/data/raw/online_retail.csv"

# Read the Excel file
df = pd.read_excel(input_file)

# Save the data as CSV
df.to_csv(output_file, index=False, encoding="utf-8")

# Confirm the conversion
print("Conversion completed!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))
print("Column names:", df.columns.tolist())