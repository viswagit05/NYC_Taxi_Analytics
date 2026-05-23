# scripts/load_to_postgres.py
"""
Business Question: We need a queryable database for the dashboard.
Decision: Use PostgreSQL for its reliability and SQL support.
"""
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# 1. CONNECT TO POSTGRES (running in Docker)
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@localhost:5432/{os.getenv('DB_NAME')}"
)

# 2. LOAD CLEANED DATA
df = pd.read_parquet('data/processed/taxi_cleaned.parquet')

# 3. LOAD IN CHUNKS (for large datasets)
chunk_size = 50000
for i in range(0, len(df), chunk_size):
    chunk = df.iloc[i:i+chunk_size]
    if i == 0:
        chunk.to_sql('taxi_trips', engine, if_exists='replace', index=False)
        print(f"Created table with first {len(chunk)} rows")
    else:
        chunk.to_sql('taxi_trips', engine, if_exists='append', index=False)
    print(f"Loaded rows {i} to {i+len(chunk)}")

print("Data loading complete!")

# 4. VERIFY
with engine.connect() as conn:
    result = conn.execute("SELECT COUNT(*) FROM taxi_trips")
    print(f"Total rows in database: {result.fetchone()[0]}")