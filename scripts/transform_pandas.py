# scripts/transform_pandas.py
"""
Business Question: What factors influence fare amounts and driver earnings?
Decision: Clean and enrich data to enable accurate analysis.
"""
import pandas as pd
import numpy as np

# 1. LOAD RAW DATA
df = pd.read_csv('data/processed/taxi_full.csv')

df = df.rename(columns={
    'tpep_pickup_datetime': 'pickup_datetime',
    'tpep_dropoff_datetime': 'dropoff_datetime'
})

print(f"Before cleaning: {len(df)} rows")

# 2. HANDLE MISSING VALUES
# Check null counts
null_counts = df.isnull().sum()
print(f"Missing values:\n{null_counts[null_counts > 0]}")

# Drop rows missing critical fields (we can't analyze without these)
critical_cols = ['fare_amount', 'trip_distance', 'pickup_datetime']
df = df.dropna(subset=critical_cols)

# For other columns, fill with default values
df['passenger_count'] = df['passenger_count'].fillna(1)  # Assume single passenger
df['payment_type'] = df['payment_type'].fillna(1)        # Assume credit card

# 3. REMOVE OUTLIERS
# Trip distance > 0 and < 100 miles (NYC to Philly is ~95 miles)
df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 100)]

# Fare amount > $2.50 (base fare) and < $500 (reasonable max)
df = df[(df['fare_amount'] >= 2.5) & (df['fare_amount'] < 500)]

# Passenger count between 1 and 6
df = df[(df['passenger_count'] >= 1) & (df['passenger_count'] <= 6)]

# 4. CONVERT DATE/TIME FORMATS
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])

# 5. CREATE NEW FEATURES (Feature Engineering)
# Trip duration in minutes
df['trip_duration_minutes'] = (
    df['dropoff_datetime'] - df['pickup_datetime']
).dt.total_seconds() / 60

# Remove unrealistic trips (duration < 1 minute or > 3 hours)
df = df[(df['trip_duration_minutes'] >= 1) & (df['trip_duration_minutes'] <= 180)]

# Time-based features
df['pickup_hour'] = df['pickup_datetime'].dt.hour
df['pickup_day_of_week'] = df['pickup_datetime'].dt.dayofweek  # 0=Monday, 6=Sunday
df['pickup_month'] = df['pickup_datetime'].dt.month

# Tip percentage (where tip amount exists)
df['tip_percentage'] = (df['tip_amount'] / df['fare_amount']) * 100
df['tip_percentage'] = df['tip_percentage'].fillna(0)

# 6. VALIDATE THE CLEANED DATA
print(f"After cleaning: {len(df)} rows ({len(df)/null_counts.sum()*100:.1f}% retained)")
print("\nData Types:")
print(df.dtypes)
print("\nSample of cleaned data:")
print(df[['fare_amount', 'trip_distance', 'trip_duration_minutes', 'pickup_hour']].head())

# 7. SAVE CLEANED DATA
df.to_parquet('data/processed/taxi_cleaned.parquet', index=False)
print("Cleaned data saved as Parquet for efficient storage")