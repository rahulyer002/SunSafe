import pandas as pd

input_file = "data/processed/skin_cancer_incidence_clean.csv"

df = pd.read_csv(input_file)

print("\nColumns:")
print(df.columns.tolist())

print("\nUnique cancer_group_site values:")
print(sorted(df["cancer_group_site"].dropna().unique()))

print("\nUnique sex values:")
print(sorted(df["sex"].dropna().unique()))

print("\nUnique age_group values:")
print(sorted(df["age_group"].dropna().unique()))