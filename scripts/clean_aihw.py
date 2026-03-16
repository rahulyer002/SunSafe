import pandas as pd

# input/output files
input_file = "data/raw/AIHW_raw.xlsx"
output_file = "data/processed/skin_cancer_incidence_clean.csv"

# read the sheet using the actual header row
# header=4 means row 5 becomes the column names
df = pd.read_excel(input_file, sheet_name="Table S1a.1", header=5)

# drop fully empty rows
df = df.dropna(how="all")

# clean column names
df.columns = df.columns.astype(str).str.strip()
df.columns = df.columns.str.replace("\n", " ", regex=False)

for col in df.columns:
    if "Age-specific rate" in col:
        df = df.rename(columns={col: "incidence_rate"})

print("\nColumns after header fix:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10))

# rename to backend-friendly names
df = df.rename(columns={
    "Cancer group/site": "cancer_group_site",
    "Year": "year",
    "Sex": "sex",
    "Age group (years)": "age_group",
    "Count": "count",
    "Age-specific rate (per 100,000)": "incidence_rate",
    "ICD10 codes": "icd10_code"
})

# keep only columns that actually exist
wanted_cols = [
    "cancer_group_site",
    "year",
    "sex",
    "age_group",
    "count",
    "incidence_rate",
    "icd10_code"
]

existing_cols = [col for col in wanted_cols if col in df.columns]
clean_df = df[existing_cols].copy()

# drop rows where year is missing
if "year" in clean_df.columns:
    clean_df = clean_df[clean_df["year"].notna()]

# save cleaned output
clean_df.to_csv(output_file, index=False)

print("\nSaved cleaned AIHW file to:")
print(output_file)

print("\nShape:")
print(clean_df.shape)

print("\nColumns:")
print(clean_df.columns.tolist())

print("\nFirst 5 rows:")
print(clean_df.head())