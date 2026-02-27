use database toys_db;

CREATE OR REPLACE VIEW "TOYS_DB"."RAW_DATA_TOYS"."V_SALES_PERFORMANCE" AS
SELECT 
    p.PRODUCT_ID as PRODUCT_ID,
    s.SALE_ID as SALE_ID,
    p.PRODUCT_NAME as PRODUCT_NAME,
    p.PRODUCT_CATEGORY as PRODUCT_CATEGORY,
    s.DATE::DATE as SALE_DATE,
    s.UNITS::INT as UNITS_SOLD,
    -- Clean Product Price from the Product Staging table
    TRY_CAST(REGEXP_REPLACE(p.PRODUCT_COST, '[^0-9.]', '') AS DECIMAL(10,2)) as UNIT_COST,
    -- Clean Product Cost from the Product Staging table
    TRY_CAST(REGEXP_REPLACE(p.PRODUCT_PRICE, '[^0-9.]', '') AS DECIMAL(10,2)) as UNIT_PRICE,
    -- Calculate Total Revenue on the fly
    (UNIT_COST * UNIT_PRICE) as TOTAL_REVENUE
FROM "TOYS_DB"."RAW_DATA_TOYS"."STG_SALES" s
JOIN "TOYS_DB"."RAW_DATA_TOYS"."STG_PRODUCTS" p 
  ON s.PRODUCT_ID = p.PRODUCT_ID; -- Joining on Product_ID
