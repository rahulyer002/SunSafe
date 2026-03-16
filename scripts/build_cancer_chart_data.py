import pandas as pd

input_file = "data/processed/skin_cancer_incidence_clean.csv"
output_file = "data/processed/skin_cancer_chart_data.csv"

df = pd.read_csv(input_file)

# Filter to a simple chart-ready subset
chart_df = df[
    (df["cancer_group_site"] == "Melanoma of the skin") &
    (df["sex"] == "Persons") &
    (df["age_group"] == "All ages combined")
].copy()

# Keep only chart-friendly fields
chart_df = chart_df[["year", "incidence_rate"]].copy()

# Add frontend/app context label
chart_df["city"] = "Melbourne"

# Sort by year
chart_df = chart_df.sort_values("year").reset_index(drop=True)

# Save result
chart_df.to_csv(output_file, index=False)

print("Saved chart data to:")
print(output_file)

print("\nShape:")
print(chart_df.shape)

print("\nColumns:")
print(chart_df.columns.tolist())

print("\nFirst 10 rows:")
print(chart_df.head(10))