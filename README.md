## Developing a Scalable Retail Forecasting Dashboard with Streamlit and Snowpark

This is a production-grade data engineering and machine learning project designed to solve a common retail challenge: inventory stockouts and revenue unpredictability. By transforming messy, raw toy sales transactions into structured, high-quality data layers, this system leverages Snowflake’s native Machine Learning capabilities to provide actionable 30-day revenue forecasts via an interactive Streamlit dashboard.  

### Key Features
Automated Forecasting: Generates a new 30-day revenue outlook with a single click.  
Data Cleaning Pipeline: Automated handling of "dirty" financial strings (e.g., removing '$' and converting to FLOAT).  
Interactive Analytics: A Streamlit UI allowing stakeholders to visualize historical performance vs. predicted growth.  

### Architecture & Data Flow
The project follows the Medallion (Lakehouse) Architecture to ensure data integrity and scalability:  
**Bronze (Raw)**: Ingestion of raw CSV sales data and product catalogs into Snowflake stages.  
**Silver (Cleaned)**: Data transformation using SQL and Python (Snowpark) to handle currency symbol removal, data type casting, and deduplication.  
**Gold (Aggregated)**: Creation of a unified V_FORECAST_INPUT view, aggregating transactions into daily revenue totals optimized for time-series analysis.

