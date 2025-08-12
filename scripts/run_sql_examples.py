import duckdb
import pandas as pd
from pathlib import Path

base = Path(__file__).resolve().parents[1]
csv_path = base / "data" / "processed" / "loads_clean.csv"
sql_path = base / "src" / "sql" / "queries.sql"

con = duckdb.connect()
con.execute(f"CREATE OR REPLACE TABLE loads AS SELECT * FROM read_csv('{csv_path.as_posix()}', header=True, auto_detect=True)")

print("Loaded table 'loads' from", csv_path)

sql_text = Path(sql_path).read_text()
# Split on semicolons that end statements
for stmt in [s.strip() for s in sql_text.split(';') if s.strip()]:
    print("\n--- Running ---\n", stmt[:120].replace("\n"," ") + ("..." if len(stmt)>120 else ""))
    try:
        res = con.execute(stmt).fetchdf()
        print(res.head(10).to_string(index=False))
    except Exception as e:
        print("Error:", e)
