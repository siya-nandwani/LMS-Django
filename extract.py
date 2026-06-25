

import pandas as pd
import pyodbc
from datetime import datetime

added_by = "ExcelImport"
added_dts = datetime.now().strftime("%H:%M:%S")

excel_file = r"C:\Users\nandw\Downloads\Product_Lead_Data_Demo.xlsx"

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=LeadManagementDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

tables = ["Product_Category", "Region", "Lead_Status", "Lead_Source",
          "Product", "Territory", "Lead", "Lead_Follow_Up"]

for table in tables:
    print(f"\nImporting {table}...")

    df = pd.read_excel(excel_file, sheet_name=table)

    # FIX: remove hidden spaces in column names
    df.columns = df.columns.str.strip()
    
    df = df.where(pd.notnull(df), None)

    df["Added_By"] = added_by
    df["Added_Dts"] = added_dts

    # IMPORTANT: rebuild columns AFTER adding
    cols = list(df.columns)
    
    sql = f"""
    INSERT INTO {table}
    ({", ".join(cols)})
    VALUES ({", ".join(["?"] * len(cols))})
    """

    for _, row in df.iterrows():
        values = [row[col] for col in cols] 
        try:
            cursor.execute(sql, values)
        
        except Exception as e:
            print(f"Error in {table}: {e}")

    conn.commit()
    print(f"{table} imported successfully ✔")

cursor.close()
conn.close()

print("\nDONE 🚀")