use database toys_db;

WITH product_margin AS(
    SELECT
        product_id, 
        product_name,
        product_category,
        (unit_price - unit_cost) AS unit_profit
    FROM "TOYS_DB"."RAW_DATA_TOYS"."V_SALES_PERFORMANCE"
),

sales_performance AS (
    SELECT
        s.store_id,
        pm.product_category,
        s.units::NUMBER * unit_profit AS total_profit
    FROM "TOYS_DB"."RAW_DATA_TOYS"."STG_SALES" s
    JOIN product_margin pm ON s.product_id = pm.product_id    
)

SELECT 
    st.c3 as store_location,
    sp.product_category,
    SUM(sp.total_profit) AS gross_profit
FROM sales_performance sp
JOIN "TOYS_DB"."RAW_DATA_TOYS"."STG_STORES" st ON sp.store_id = st.c1
GROUP BY 1, 2
ORDER BY 3 DESC;


