
CREATE TABLE IF NOT EXISTS customers (
    CustomerID VARCHAR(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS products (
    StockCode VARCHAR(20)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_0900_as_cs
        PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS transactions (
    TransactionID BIGINT AUTO_INCREMENT PRIMARY KEY,
    InvoiceNo VARCHAR(10) NOT NULL,
    StockCode VARCHAR(20)
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_0900_as_cs
        NOT NULL,
    Description VARCHAR(100),
    Quantity INT NOT NULL,
    InvoiceDate DATETIME NOT NULL,
    UnitPrice DECIMAL(12,3) NOT NULL,
    CustomerID VARCHAR(20),
    Country VARCHAR(50) NOT NULL,
    TransactionType VARCHAR(20) NOT NULL,

    CONSTRAINT fk_transaction_customer
        FOREIGN KEY (CustomerID)
        REFERENCES customers(CustomerID),

    CONSTRAINT fk_transaction_product
        FOREIGN KEY (StockCode)
        REFERENCES products(StockCode)
);
