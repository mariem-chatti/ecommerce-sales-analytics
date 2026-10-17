
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# --------------------------------------------------
# 1. READ CLEANED DATA
# --------------------------------------------------

df = pd.read_csv(
    "/app/data/processed/online_retail_cleaned.csv",
    dtype={
        "InvoiceNo": "string",
        "StockCode": "string",
        "CustomerID": "string"
    }
)

# --------------------------------------------------
# 2. CONNECT TO MYSQL
# --------------------------------------------------

url = URL.create(
    drivername="mysql+pymysql",
    username=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    host="mysql",
    port=3306,
    database=os.environ["MYSQL_DATABASE"]
)

engine = create_engine(url)

with engine.connect() as connection:
    database = connection.execute(
        text("SELECT DATABASE()")
    ).scalar()

print("Connected to database:", database)

# --------------------------------------------------
# 3. PREPARE DATA
# --------------------------------------------------

customers = (
    df[["CustomerID"]]
    .dropna()
    .drop_duplicates()
)

products = (
    df[["StockCode"]]
    .dropna()
    .drop_duplicates()
)

transactions = df[
    [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
        "TransactionType"
    ]
].copy()

transactions["InvoiceDate"] = pd.to_datetime(
    transactions["InvoiceDate"]
)

expected_counts = {
    "customers": len(customers),
    "products": len(products),
    "transactions": len(transactions)
}

# --------------------------------------------------
# 4. CHECK EXISTING DATA
# --------------------------------------------------

with engine.connect() as connection:
    actual_counts = {
        table: connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar_one()
        for table in expected_counts
    }

print("Expected row counts:", expected_counts)
print("Current database counts:", actual_counts)

if actual_counts == expected_counts:
    print("All tables already populated. Nothing to import.")

elif all(count == 0 for count in actual_counts.values()):

    # --------------------------------------------------
    # 5. IMPORT CUSTOMERS
    # --------------------------------------------------

    customers.to_sql(
        name="customers",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )

    print("Customers imported successfully!")

    # --------------------------------------------------
    # 6. IMPORT PRODUCTS
    # --------------------------------------------------

    products.to_sql(
        name="products",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )

    print("Products imported successfully!")

    # --------------------------------------------------
    # 7. IMPORT TRANSACTIONS
    # --------------------------------------------------

    transactions.to_sql(
        name="transactions",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000
    )

    print("Transactions imported successfully!")

    # --------------------------------------------------
    # 8. VERIFY IMPORT
    # --------------------------------------------------

    with engine.connect() as connection:
        final_counts = {
            table: connection.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar_one()
            for table in expected_counts
        }

    if final_counts != expected_counts:
        raise RuntimeError(
            f"Import verification failed: {final_counts}"
        )

    print("All row counts verified successfully!")

else:
    raise RuntimeError(
        "Database is partially populated or row counts "
        "do not match the dataset. Import stopped to "
        "prevent duplicate records."
    )

engine.dispose()
