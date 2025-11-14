import pandas as pd
import sqlite3
import os

# ------------------ File Paths ------------------
DATA_PATH = os.path.join("..", "data", "Spaza_products_messy.xlsx")
DB_PATH = os.path.join("..", "db", "spaza_shop.db")
CLEANED_PATH = os.path.join("..", "data", "cleaned_products.xlsx")
CSV_PATH = os.path.join("..", "data", "powerbi_products.csv")

print("Checking file path:", os.path.abspath(DATA_PATH))

# ------------------ Load Excel ------------------
try:
    df = pd.read_excel(DATA_PATH)
    print(f"Loaded messy data with {df.shape[0]} rows and {df.shape[1]} columns")
except Exception as e:
    print("Error loading Excel file:", e)
    exit()

# Show first 5 rows
print("\nFirst few rows of messy data:")
print(df.head())

# ------------------ Clean Column Names ------------------
df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]
print("Columns after cleaning:", df.columns.tolist())

# ------------------ Drop Duplicates & Empty Rows ------------------
df.drop_duplicates(inplace=True)
df.dropna(how="all", inplace=True)

# ------------------ Convert Columns to Correct Types ------------------
if "price" in df.columns:
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

for col in ['quantity', 'stockqty']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

for col in ['date_added', 'expire_date', 'dateadded']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# ------------------ Handle Missing Values ------------------

# 1️⃣ Product Name (auto-detect column containing 'product' and 'name')
product_col = None
for col in df.columns:
    if 'product' in col and 'name' in col:
        product_col = col
        break

if product_col is None:
    raise ValueError("No product name column found in the dataset!")

# Drop rows missing product name
df.dropna(subset=[product_col], inplace=True)

# 2️⃣ Price
df['missing_price'] = df['price'].isna()
df['price'].fillna(0, inplace=True)

# 3️⃣ Barcode (convert to string to avoid dtype warning)
if 'barcode' in df.columns:
    df['barcode'] = df['barcode'].astype(str)
    df['barcode'].fillna('UNKNOWN', inplace=True)
    # Flag missing barcode
    df['missing_barcode'] = df['barcode'].isin(['nan', 'None', 'UNKNOWN'])

# 4️⃣ Category
if 'category' in df.columns:
    df['category'].fillna('Unknown', inplace=True)
    df['category'] = df['category'].astype(str).str.title()

# 5️⃣ Quantity / Stock
for col in ['quantity', 'stockqty']:
    if col in df.columns:
        df[f'missing_{col}'] = df[col].isna()
        df[col].fillna(0, inplace=True)

# 6️⃣ Supplier / Brand
for col in ['supplier', 'brand']:
    if col in df.columns:
        df[f'missing_{col}'] = df[col].isna()
        df[col].fillna('Unknown', inplace=True)

# ------------------ Save Cleaned Excel ------------------
df.to_excel(CLEANED_PATH, index=False)
print(f"\nCleaned data saved to: {CLEANED_PATH}")

# ------------------ Save to SQLite ------------------
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
df.to_sql("products", conn, if_exists="replace", index=False)
conn.close()
print(f"Data successfully loaded into SQLite database: {DB_PATH}")

# ------------------ Export CSV for Power BI ------------------
df.to_csv(CSV_PATH, index=False)
print(f"CSV for Power BI exported to: {CSV_PATH}")

# ------------------ Summary ------------------
print("\nData Cleaning Summary")
print(f"Total products: {len(df)}")
print(f"Products with missing price: {df['missing_price'].sum()}")
if 'missing_barcode' in df.columns:
    print(f"Products with missing barcode: {df['missing_barcode'].sum()}")
for col in ['missing_quantity', 'missing_stockqty', 'missing_supplier', 'missing_brand']:
    if col in df.columns:
        print(f"{col.replace('missing_', '').capitalize()} missing: {df[col].sum()}")
print(f"Product name column used: {product_col}")
