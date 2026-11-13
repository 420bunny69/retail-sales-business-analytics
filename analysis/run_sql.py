
import pandas as pd
import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load dataset
df = pd.read_csv(
    BASE_DIR / "data" / "Sample - Superstore.csv",
    encoding="latin1"
)

# Convert dates to SQLite-compatible format
df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="%m/%d/%Y"
).dt.strftime("%Y-%m-%d")

# Create SQLite database
conn = sqlite3.connect(BASE_DIR / "superstore.db")

# Store dataset in database
df.to_sql("superstore", conn, if_exists="replace", index=False)

# Read SQL queries
sql_file = BASE_DIR / "sql" / "analysis.sql"

with open(sql_file, "r", encoding="utf-8") as file:
    sql_content = file.read()

# Execute queries individually
queries = [
    query.strip()
    for query in sql_content.split(";")
    if query.strip()
]

for i, query in enumerate(queries, 1):
    if query.startswith("--"):
        query = query[query.upper().find("SELECT"):]

    print(f"\n{'='*50}")
    print(f"QUERY {i}")
    print("="*50)

    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()

print("\nAll SQL queries executed successfully!")
