import pandas as pd

# ARPANSA
arpansa_file = "data/raw/arpansa_melbourne_2024_raw.csv"

print("\n========== ARPANSA 2024 ==========")
uv_df = pd.read_csv(arpansa_file)

print("\nShape:")
print(uv_df.shape)

print("\nColumns:")
print(uv_df.columns.tolist())

print("\nFirst 5 rows:")
print(uv_df.head())

print("\nData types:")
print(uv_df.dtypes)

print("\nMissing values:")
print(uv_df.isnull().sum())


#AIHW
aihw_file = "data/raw/AIHW_raw.xlsx"

print("\n========== AIHW SHEETS ==========")
xls = pd.ExcelFile(aihw_file)
print(xls.sheet_names)

# change this if needed after checking output
sheet_name = "Table S1a.1"

print(f"\n========== AIHW: {sheet_name} ==========")
cancer_df = pd.read_excel(aihw_file, sheet_name=sheet_name)

print("\nShape:")
print(cancer_df.shape)

print("\nColumns:")
print(cancer_df.columns.tolist())

print("\nFirst 10 rows:")
print(cancer_df.head(10))

print("\nData types:")
print(cancer_df.dtypes)

print("\nMissing values:")
print(cancer_df.isnull().sum())