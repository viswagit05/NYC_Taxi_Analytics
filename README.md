# NYC Taxi Analytics

A Streamlit dashboard for NYC taxi trip analytics using DuckDB.

## Repo structure

- `scripts/` — ingestion, transformation, visualization scripts
- `data/processed/` — cleaned dataset used by the dashboard
- `sql/` — example analytical queries
- `notebooks/` — exploration notebooks
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.14
- `streamlit`
- `duckdb`
- `pandas`

## Run locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

   python -m streamlit run scripts/visualize.py
