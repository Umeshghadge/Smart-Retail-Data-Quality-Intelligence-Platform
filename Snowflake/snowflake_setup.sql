-- Smart Retail Analytics
-- Snowflake Setup and Data Loading

-- 1. Create database

CREATE DATABASE IF NOT EXISTS RETAIL_PROJECT;

USE DATABASE RETAIL_PROJECT;


-- 2. Create schema

CREATE SCHEMA IF NOT EXISTS RETAIL_ANALYTICS;

USE SCHEMA RETAIL_ANALYTICS;


-- 3. Create warehouse

CREATE WAREHOUSE IF NOT EXISTS RETAIL_WH
WITH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;


-- 4. Create CSV file format

CREATE FILE FORMAT IF NOT EXISTS RETAIL_CSV_FORMAT
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
SKIP_HEADER = 1;


-- 5. Create internal stage

CREATE STAGE IF NOT EXISTS RETAIL_STAGE;


-- 6. Create target table

CREATE TABLE IF NOT EXISTS RETAIL_CLEANED
(
    Invoice STRING,
    StockCode STRING,
    Description STRING,
    Quantity NUMBER,
    Invoice_Date TIMESTAMP,
    Price FLOAT,
    "Customer ID" FLOAT,
    Country STRING,
    Revenue FLOAT,
    Customer_ID_Missing BOOLEAN,
    Year NUMBER,
    Month NUMBER,
    Month_Name STRING,
    Transaction_Type STRING,
    Customer_Type STRING,
    Revenue_Category STRING,
    Quantity_Category STRING,
    StockCode_Type STRING
);


-- 7. Upload processed CSV to stage
-- Executed using SnowSQL

PUT 'file:///D:/path/retail_cleaned.csv'
@RETAIL_STAGE
AUTO_COMPRESS = TRUE
PARALLEL = 1;


-- 8. Check uploaded files

LIST @RETAIL_STAGE;


-- 9. Load data into table

COPY INTO RETAIL_CLEANED
FROM @RETAIL_STAGE/retail_cleaned.csv.gz
FILE_FORMAT = (
    FORMAT_NAME = RETAIL_CSV_FORMAT
)
ON_ERROR = 'CONTINUE';


-- 10. Validate row count

SELECT COUNT(*) AS total_rows
FROM RETAIL_CLEANED;


-- 11. Check missing Customer IDs

SELECT COUNT(*) AS missing_customer_id
FROM RETAIL_CLEANED
WHERE "Customer ID" IS NULL;


-- 12. Check transaction types

SELECT
    Transaction_Type,
    COUNT(*) AS total_records,
    SUM(Revenue) AS total_revenue
FROM RETAIL_CLEANED
GROUP BY Transaction_Type
ORDER BY total_records DESC;


-- 13. Check price-related records

SELECT
    COUNT_IF(Price = 0) AS zero_price_records,
    COUNT_IF(Price < 0) AS negative_price_records
FROM RETAIL_CLEANED;


-- 14. Customer revenue analysis

SELECT
    "Customer ID",
    SUM(Revenue) AS total_revenue
FROM RETAIL_CLEANED
WHERE "Customer ID" IS NOT NULL
GROUP BY "Customer ID"
ORDER BY total_revenue DESC
LIMIT 10;


-- 15. Monthly revenue analysis

SELECT
    Year,
    Month,
    Month_Name,
    SUM(Revenue) AS monthly_revenue
FROM RETAIL_CLEANED
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;