# SpazaShop Inventory Data Cleaner & Loader

This project provides a Python script to clean messy inventory data from Excel and load it into a SQLite database for further analysis or application use.

---

## Features

- Loads messy product data from an Excel file.
- Cleans the data by:
  - Normalizing column names
  - Dropping duplicate rows
  - Removing completely empty rows
  - Converting numeric columns (like `price`) to proper data types
  - Filling missing values with sensible defaults (mean for `price`, `"Unknown"` for `category`)
- Saves a cleaned Excel version of the data.
- Loads the cleaned data into a SQLite database.

---

## Requirements

- Python 3.8+
- Pandas
- SQLite3 (built-in with Python)
- OpenPyXL (for Excel file reading/writing)

Install dependencies with:

```bash
pip install pandas openpyxl


////////////////////////////////////////////////////////////////////////////
project-root/
│
├─ data/
│   ├─ Spaza_products_messy.xlsx   # Original messy Excel data
│   └─ cleaned_products.xlsx       # Cleaned Excel data (generated)
│
├─ db/
│   └─ spaza_shop.db               # SQLite database (generated)
│
└─ scripts/
    └─ clean_and_load.py           # Main Python script
    |_ display_database.py         # Script to display database that has been save on SQlite

///////////////////////////////////////////////////////////////////////////////



