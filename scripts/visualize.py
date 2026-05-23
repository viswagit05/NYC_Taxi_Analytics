# scripts/visualize.py
import streamlit as st
import pandas as pd
import duckdb

st.set_page_config(page_title="NYC Taxi Analytics", layout="wide")

# 1. CONNECT TO DUCKDB
conn = duckdb.connect('nyc_taxi.duckdb')

st.title("🚖 NYC Taxi Trip Analytics Dashboard")
st.markdown("## Business Insights from NYC Yellow Taxi Data")

# 2. SIDEBAR FILTERS
st.sidebar.header("Filters")
min_fare = st.sidebar.slider("Minimum Fare ($)", 0, 100, 0)
date_range = st.sidebar.date_input("Date Range", [])

# 3. KPI METRICS
total_trips = conn.execute("SELECT COUNT(*) FROM taxi_trips").fetchone()[0]
total_revenue = conn.execute("SELECT SUM(fare_amount) FROM taxi_trips").fetchone()[0]
avg_tip = conn.execute("SELECT AVG(tip_percentage) FROM taxi_trips").fetchone()[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Trips", f"{total_trips:,}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Average Tip", f"{avg_tip:.2f}%")

# 4. PEAK HOURS CHART
st.subheader("📊 Trip Volume by Hour")
hourly_trips = conn.execute("""
    SELECT pickup_hour, COUNT(*) as trips 
    FROM taxi_trips 
    GROUP BY pickup_hour 
    ORDER BY pickup_hour
""").fetchdf()
st.bar_chart(hourly_trips.set_index('pickup_hour'))

# 5. REVENUE BY DAY
st.subheader("💰 Revenue by Day of Week")
daily_revenue = conn.execute("""
    SELECT pickup_day_of_week, SUM(fare_amount) as revenue 
    FROM taxi_trips 
    GROUP BY pickup_day_of_week 
    ORDER BY pickup_day_of_week
""").fetchdf()
st.line_chart(daily_revenue.set_index('pickup_day_of_week'))

# 6. PAYMENT METHOD BREAKDOWN
st.subheader("💳 Payment Method Distribution")
payment_stats = conn.execute("""
    SELECT 
        CASE payment_type
            WHEN 1 THEN 'Credit Card'
            WHEN 2 THEN 'Cash'
            ELSE 'Other'
        END as method,
        COUNT(*) as trips,
        AVG(fare_amount) as avg_fare
    FROM taxi_trips
    GROUP BY payment_type
""").fetchdf()
st.dataframe(payment_stats)

# 7. TOP QUERIES SECTION
st.subheader("🔍 Business Insights")
insights = conn.execute("""
    SELECT 
        'Peak hours generate highest volume between 4-7 PM' as insight,
        (SELECT AVG(fare_amount) FROM taxi_trips WHERE pickup_hour BETWEEN 16 AND 19) as peak_avg_fare,
        (SELECT AVG(fare_amount) FROM taxi_trips WHERE pickup_hour NOT BETWEEN 16 AND 19) as off_peak_avg_fare
""").fetchone()

st.metric("Peak Hour Avg Fare vs Off-Peak", 
          f"${insights[1]:.2f}", 
          delta=f"${insights[1] - insights[2]:.2f} higher")

conn.close()