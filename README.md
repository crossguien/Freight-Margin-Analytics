# Freight Margin Analytics (Portfolio Project)

**Why this project matters:** As a data analyst working with logistics or operations teams, you’ll often be asked to explain *where margin comes from*, *which customers and lanes are profitable*, and *what operational factors (like on‑time performance or detention) erode profit*.  
This repo is an end‑to‑end, business-style project that demonstrates SQL, Python, and visualization skills on a realistic freight dataset you can fully run locally.

## Key Business Questions
- Which **shippers** and **lanes** (origin→destination states) drive the most **gross margin**?
- How does **on‑time performance**, **detention**, and **equipment type** impact **margin %**?
- Where are the **leaks**: high revenue but **low margin**, or frequent **late deliveries**?
- What are the **top opportunities** to improve **profit per load**?

## Tech & Skills Demonstrated
- **Python** (pandas, numpy) for data generation, cleaning, features
- **SQL** (DuckDB) for slicing KPIs quickly
- **Matplotlib** for simple visuals (save-to-file)
- **Testing** with `pytest` for KPI calculations
- **Project structure**: `src/`, `notebooks/`, `data/`, `reports/`, `tests/`

## Quickstart

```bash
# 1) Create env (recommend uv, conda, or venv). Example with pip:
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Generate data and KPIs
python src/etl.py

# 3) (Optional) Run the notebook
jupyter notebook notebooks/01_explore.ipynb

# 4) (Optional) Run example SQL with DuckDB
python scripts/run_sql_examples.py

# 5) (Optional) Run tests
pytest -q
```

**Outputs:**  
- Cleaned dataset at `data/processed/loads_clean.csv`  
- Saved charts in `reports/figures/`  
- Example SQL queries in `src/sql/queries.sql`

## Repo Structure
```
freight-margin-analytics/
├── data/
│   ├── raw/                 # synthetic source tables
│   └── processed/           # cleaned, enriched tables
├── notebooks/
│   └── 01_explore.ipynb     # EDA & visuals
├── reports/
│   └── figures/             # saved charts
├── scripts/
│   └── run_sql_examples.py  # executes sample SQL with DuckDB
├── src/
│   ├── etl.py               # generates synthetic data, cleans, features, charts
│   ├── metrics.py           # KPI functions (margin, OTP, lane stats)
│   └── sql/
│       └── queries.sql      # ready-to-run SQL snippets
├── tests/
│   └── test_metrics.py      # unit tests
├── .gitignore
├── requirements.txt
└── README.md
```

> Tip: If you want to extend this, add a **Tableau** or **Power BI** dashboard pointing at `data/processed/loads_clean.csv` and replicate the SQL KPIs visually.

## License
MIT
