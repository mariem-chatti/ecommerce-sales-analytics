# E-Commerce Sales Analytics

## Project Overview

An end-to-end data analytics project using historical e-commerce transactions to explore sales performance, customer behavior, and product trends.

The project demonstrates a practical data analytics workflow, from raw data ingestion and cleaning to relational database design, SQL-based analysis, and eventually interactive business intelligence dashboards.

Python and MySQL run in separate Docker containers managed by Docker Compose.

## Version 1 — Sales Analytics

Version 1 focuses on:

- Data ingestion, exploration, and cleaning using Python and Pandas
- Relational data modeling and storage using MySQL
- SQL-based business analysis
- Exploratory data analysis and statistics
- Customer segmentation
- Interactive dashboards using Power BI

**Current progress:** Data cleaning, database creation, and data loading are complete. SQL analytics is in progress. Customer segmentation and dashboards are planned.

## Dataset

**Source:** [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)

The dataset contains historical transactions from a UK-based online retailer between December 2010 and December 2011.

The original dataset contains 541,909 records with the following columns:

| Column | Description |
|---|---|
| InvoiceNo | Invoice identifier |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of units recorded |
| InvoiceDate | Date and time of the transaction |
| UnitPrice | Unit price in GBP |
| CustomerID | Customer identifier, when available |
| Country | Customer's country of residence |

### Dataset Processing Summary

| Metric | Count |
|---|---:|
| Original records | 541,909 |
| Exact duplicate records removed | 5,268 |
| Cleaned transaction records | 536,641 |
| Unique known customers | 4,372 |
| Unique product identifiers | 4,070 |
| Transactions with missing CustomerID | 135,037 |

The cleaned dataset is saved as `data/processed/online_retail_cleaned.csv`.

## Technology Stack

**Currently implemented:**

- Python 3.11
- Pandas and NumPy
- MySQL 8.4
- SQL and SQLAlchemy
- PyMySQL
- Docker and Docker Compose
- Git and GitHub

**Planned:**

- Power BI for interactive dashboards
- Additional statistical analysis and customer segmentation

## Project Architecture

The data pipeline follows this workflow:

```text
UCI Online Retail Dataset
           |
           v
     Raw Dataset
           |
           v
   Python + Pandas
   Data Exploration
   Data Cleaning
   Classification
           |
           v
   Cleaned CSV File
           |
           v
   Python + SQLAlchemy
           |
           v
       MySQL 8.4
   -------------------
   |    Customers    |
   |    Products     |
   |    Transactions |
   -------------------
           |
           v
      SQL Analytics
           |
           v
   Power BI Dashboards
        (Planned)
```

Docker Compose manages the Python application and MySQL database as separate services.

## Data Cleaning and Preparation

Data cleaning is performed using Python and Pandas.

### 1. Duplicate Removal

The original dataset contained 5,268 exact duplicate records.

These duplicates were removed, reducing the dataset from 541,909 to 536,641 rows.

### 2. Missing Values

Missing values were investigated before deciding how to handle them.

In particular, 135,037 cleaned records have missing `CustomerID` values.

These transactions were preserved because they still contain useful sales and product information.

Missing CustomerIDs are stored as SQL `NULL` values in the transactions table. No artificial customer identifiers were generated.

### 3. Transaction Classification

A new column, `TransactionType`, was introduced to distinguish different transaction categories.

| Transaction Type | Records |
|---|---:|
| SALE | 524,878 |
| CANCELLATION | 9,251 |
| ADJUSTMENT | 1,336 |
| ZERO_PRICE | 1,174 |
| BAD_DEBT | 2 |
| **Total** | **536,641** |

This classification allows business analyses to include or exclude particular transaction types depending on the metric being calculated.

For example, gross sales revenue is calculated using only transactions classified as `SALE`.

### 4. Data Type Preparation

Identifiers such as `InvoiceNo`, `StockCode`, and `CustomerID` are handled as strings.

`InvoiceDate` is converted into a datetime representation before loading it into MySQL.

The original product identifiers are preserved, including differences in capitalization.

## Database Design

The cleaned dataset is stored in a relational MySQL database named `ecommerce`.

The database contains three tables.

### Customers

Stores unique known customer identifiers.

| Column | Type | Constraint |
|---|---|---|
| CustomerID | VARCHAR(20) | Primary Key |

### Products

Stores unique product identifiers.

| Column | Type | Constraint |
|---|---|---|
| StockCode | VARCHAR(20) | Primary Key |

The `StockCode` column uses the case-sensitive collation `utf8mb4_0900_as_cs`.

### Transactions

Stores the cleaned transaction records.

| Column | Type | Description |
|---|---|---|
| TransactionID | BIGINT | Auto-increment primary key |
| InvoiceNo | VARCHAR(10) | Invoice identifier |
| StockCode | VARCHAR(20) | Foreign key referencing products |
| Description | VARCHAR(100) | Product description |
| Quantity | INT | Recorded quantity |
| InvoiceDate | DATETIME | Transaction date and time |
| UnitPrice | DECIMAL(12,3) | Unit price |
| CustomerID | VARCHAR(20) | Nullable foreign key referencing customers |
| Country | VARCHAR(50) | Customer country |
| TransactionType | VARCHAR(20) | Transaction classification |

### Relationships

- One customer can be associated with multiple transaction records.
- One product can appear in multiple transaction records.
- Each transaction record references one product.
- A transaction can have a missing customer identifier.

`Description` remains in the transactions table because the same StockCode can have multiple descriptions in the original data.

`Country` also remains in transactions rather than customers, preserving the country value recorded for each transaction.

The full database schema is available in [`sql/schema.sql`](sql/schema.sql).

## Technical Challenges and Solutions

### Case-Sensitive Product Identifiers

During product loading, MySQL raised a duplicate primary-key error.

Investigation revealed that Pandas treated identifiers such as `15056BL` and `15056bl` as different strings, while MySQL's default case-insensitive collation treated them as equal.

**Solution:**

The `StockCode` columns in both `products` and `transactions` were configured with the case-sensitive collation `utf8mb4_0900_as_cs`.

This preserves the original identifiers and allows them to coexist in the database.

### Missing Customer Identifiers

Some transactions do not contain a CustomerID.

Instead of deleting these records, the database permits `NULL` in `transactions.CustomerID`.

The customers table contains only known, unique identifiers.

### Preventing Accidental Duplicate Imports

The Python loading script checks the number of records already present in each database table.

If the tables already contain the expected row counts, the script skips importing.

If the database is partially populated or the counts do not match, the script stops rather than automatically appending potentially duplicate records.

This provides a basic safeguard against accidental repeated imports.

## Running the Project

### Prerequisites

- Docker Desktop with Docker Compose
- Git
- The UCI Online Retail dataset

### 1. Clone the Repository

```bash
git clone https://github.com/mariem-chatti/ecommerce-sales-analytics.git
cd ecommerce-sales-analytics
```

### 2. Configure Environment Variables

Create a `.env` file with the MySQL configuration expected by `docker-compose.yml`.

Do not commit `.env` files containing passwords or other credentials.

### 3. Start Docker Services

```bash
docker compose up -d --build
```

### 4. Prepare the Dataset

Place the original dataset in the appropriate raw-data directory and execute the project's data preparation and cleaning scripts.

The loading script expects the cleaned dataset at:

```text
data/processed/online_retail_cleaned.csv
```

### 5. Create the Database Tables

The SQL schema is stored in `sql/schema.sql`.

With the MySQL service running, the schema can be executed using:

```powershell
Get-Content .\sql\schema.sql -Raw | docker compose exec -T mysql mysql -u analyst -p ecommerce
```

Enter the database password when prompted.

The schema creates the `customers`, `products`, and `transactions` tables, including their primary keys, foreign keys, and product-code collations.

### 6. Load the Cleaned Data

```bash
docker compose run --rm python-app python src/load_to_mysql.py
```

The script connects to MySQL, prepares the customer, product, and transaction data, and imports it into the corresponding tables.

### 7. Access MySQL

```bash
docker compose exec mysql mysql -u analyst -p ecommerce
```

### 8. Validate the Database

```sql
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM transactions;
```

Expected results:

| Table | Records |
|---|---:|
| customers | 4,372 |
| products | 4,070 |
| transactions | 536,641 |

## SQL Business Analytics

SQL analysis is performed directly against the MySQL database.

The queries are stored in [`sql/sales_analysis.sql`](sql/sales_analysis.sql).

### Analysis 1 — Gross Sales Revenue

**Business question:** How much gross revenue was generated by sales transactions?

```sql
SELECT
    ROUND(SUM(Quantity * UnitPrice), 2) AS GrossSalesRevenue
FROM transactions
WHERE TransactionType = 'SALE';
```

**Result: £10,642,110.80**

This metric includes only records classified as `SALE` and does not subtract cancellations or other adjustments.

### Analysis 2 — Monthly Sales Performance

**Business question:** How does gross sales revenue change from month to month?

The analysis groups transactions by year and month, counts distinct invoices, and calculates monthly gross revenue.

This analysis is in progress.

### Planned Analyses

- Top-selling products by revenue and quantity
- Sales performance by country
- Customer purchasing behavior
- Customer segmentation
- Additional exploratory statistics

## Project Status

**Version 1 — In development**

**Completed:**
- Dataset exploration and cleaning
- Transaction classification
- Dockerized Python and MySQL environment
- Relational database schema
- Data loading with SQLAlchemy
- Database validation
- Initial gross sales revenue analysis

**In progress:**
- SQL business analytics

**Planned:**
- Customer segmentation
- Interactive Power BI dashboards

## Future Extension — Version 2

The project will later be extended with:

- Dimensional modeling
- Data warehousing concepts
- HDFS
- Apache Hive

The goal of Version 2 is to explore how the analytical workflow can evolve from a relational database implementation toward a larger-scale data platform.
