import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd

session = get_active_session()

st.title("Maven Toys Analysis Portal")
st.write("Real-time Time-Series Revenue Tracker")

categories_df = session.sql("SELECT DISTINCT PRODUCT_CATEGORY FROM V_SALES_PERFORMANCE").collect()
categories = [row['PRODUCT_CATEGORY'] for row in categories_df]
selected_category = st.sidebar.multiselect("Select Categories", categories, default=categories[:2])

query = f"""
    SELECT SALE_DATE, SUM(TOTAL_REVENUE) as REVENUE
    FROM V_SALES_PERFORMANCE
    WHERE PRODUCT_CATEGORY IN ({str(selected_category)[1:-1]})
    GROUP BY 1 ORDER BY 1
"""
data = session.sql(query).to_pandas()

# Display Metric Cards
total_rev = data['REVENUE'].sum()
st.metric("Total Revenue for Selection", f"${total_rev:,.2f}")

# Plot the Time-Series Chart
st.subheader("Revenue Over Time")
st.line_chart(data.set_index('SALE_DATE'))

# Show Top Products Table
st.subheader("Top Performing Products")
top_products = session.sql("""
    SELECT PRODUCT_NAME, SUM(TOTAL_REVENUE) as REVENUE
    FROM V_SALES_PERFORMANCE
    GROUP BY 1 ORDER BY 2 DESC LIMIT 10
""").to_pandas()
st.dataframe(top_products, use_container_width=True)

# 1. Run the Forecast (Snowflake returns columns: TS, FORECAST, LOWER_BOUND, UPPER_BOUND)
forecast_query = "CALL TOY_REVENUE_FORECASTER!FORECAST(FORECASTING_PERIODS => 30)"
forecast_df = session.sql(forecast_query).to_pandas()

# 2. Get Historical Data (You already renamed these to DATE and ACTUAL in the SQL string)
history_query = "SELECT SALE_DATE as DATE, DAILY_REVENUE as ACTUAL FROM V_FORECAST_INPUT"
history_df = session.sql(history_query).to_pandas()

# 3. rename to match the history_df columns ('DATE') for the merge
forecast_df = forecast_df[['"TS"', '"FORECAST"']].rename(columns={'"TS"': 'DATE', '"FORECAST"': 'PREDICTED'})

# 4. Merge them
final_df = pd.concat([history_df, forecast_df], ignore_index=True)

# 5. Plot it!
st.subheader("Historical Sales vs. 30-Day Forecast")
st.line_chart(final_df.set_index('DATE'))

## Revenue Metric Card

# Calculate the total predicted revenue for the next 30 days
total_forecasted = forecast_df['PREDICTED'].sum()

# Display as a "Metric" card
st.metric(label="Predicted Revenue (Next 30 Days)", value=f"${total_forecasted:,.2f}")

