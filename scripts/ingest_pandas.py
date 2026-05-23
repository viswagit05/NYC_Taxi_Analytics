# scripts/ingest_pandas.py
"""
Business Question: We need raw trip data in a structured format for analysis.
Decision: Use Pandas for initial exploration because we're starting small.
"""
import pandas as pd
import os
from datetime import datetime

# 1. DOWNLOAD (one-time)
# Manual step: Download yellow_tripdata_2025-01.parquet from NYC TLC website
# Place it in data/raw/

# 2. LOAD
df = pd.read_parquet('data/raw/yellow_tripdata_2025-01.parquet')

# 3. QUICK INSPECTION (always do this)
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(df.head())

# 4. SAVE SAMPLE FOR FAST EXPLORATION
# Take 1% sample for quick testing
sample_df = df.sample(frac=0.01, random_state=42)
sample_df.to_csv('data/processed/taxi_sample.csv', index=False)
print("Sample saved for fast exploration")

# 5. SAVE FULL DATA (we'll clean in next step)
df.to_csv('data/processed/taxi_full.csv', index=False)
print("Full dataset saved")