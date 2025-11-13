import pandas as pd
import sqlite3
import os

DATA_PATH = os.path.join("..", "data", "Spaza_products_messy.xlsx")
DB_PATH = os.path.join("..", "db", "spaza_shop.db")
CLEANED_PATH = os.path.join("..", "data", "cleaned_products.xlsx")

print(" Checking file path:", os.path.abspath(DATA_PATH))

# Load messy Excel data
try:
    df = pd.read_excel(DATA_PATH)
    print(f"Loaded messy data with {df.shape[0]} rows and {df.shape[1]} columns")
except Exception as e:
    print("Error loading Excel file:", e)
    exit()

# Show first 5 rows
print("\n First few rows of messy data:")
print(df.head())

# Clean column names
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

# Drop duplicates
df.drop_duplicates(inplace=True)

# Drop completely empty rows
df.dropna(how="all", inplace=True)

# Convert 'price' column to numeric, invalid parsing will be set as NaN
df['price'] = pd.to_numeric(df['price'], errors='coerce')


# Fill missing values
if "price" in df.columns:
    df["price"].fillna(df["price"].mean(), inplace=True)
if "category" in df.columns:
    df["category"].fillna("Unknown", inplace=True)

# Save cleaned file
df.to_excel(CLEANED_PATH, index=False)
print(f"\n💾 Cleaned data saved to: {CLEANED_PATH}")

# Save to SQLite
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
df.to_sql("products", conn, if_exists="replace", index=False)
conn.close()

print(f"📦 Data successfully loaded into SQLite database: {DB_PATH}")
