import pandas as pd

# Input files
uv_file = "data/processed/uv_historical_melbourne_all_years_clean.csv"
cancer_chart_file = "data/processed/skin_cancer_chart_data.csv"

# Output files
uv_yearly_file = "data/processed/chart_uv_yearly_avg.csv"
uv_monthly_file = "data/processed/chart_uv_monthly_avg.csv"
uv_monthly_max_file = "data/processed/chart_uv_monthly_max.csv"
uv_hourly_file = "data/processed/chart_uv_hourly_avg.csv"
cancer_out_file = "data/processed/chart_skin_cancer_trend.csv"

# Load datasets
uv_df = pd.read_csv(uv_file)
cancer_df = pd.read_csv(cancer_chart_file)

# Ensure datetime is parsed
uv_df["date_time"] = pd.to_datetime(uv_df["date_time"], errors="coerce")

# Yearly average UV
uv_yearly = (
    uv_df.groupby("year", as_index=False)["uv_index"]
    .mean()
    .rename(columns={"uv_index": "avg_uv_index"})
)

uv_yearly.to_csv(uv_yearly_file, index=False)

# Monthly average UV
uv_monthly = (
    uv_df.groupby(["year", "month"], as_index=False)["uv_index"]
    .mean()
    .rename(columns={"uv_index": "avg_uv_index"})
)

uv_monthly.to_csv(uv_monthly_file, index=False)

# Monthly max UV
uv_monthly_max = (
    uv_df.groupby(["year", "month"], as_index=False)["uv_index"]
    .max()
    .rename(columns={"uv_index": "max_uv_index"})
)

uv_monthly_max.to_csv(uv_monthly_max_file, index=False)

# Hourly average UV pattern
uv_hourly = (
    uv_df.groupby("hour", as_index=False)["uv_index"]
    .mean()
    .rename(columns={"uv_index": "avg_uv_index"})
)

uv_hourly.to_csv(uv_hourly_file, index=False)

# Cancer trend chart data
cancer_chart = cancer_df.copy()
cancer_chart.to_csv(cancer_out_file, index=False)

# Print summary
print("Saved chart datasets:")
print("-", uv_yearly_file)
print("-", uv_monthly_file)
print("-", uv_monthly_max_file)
print("-", uv_hourly_file)
print("-", cancer_out_file)

print("\nPreview: yearly UV")
print(uv_yearly.head())

print("\nPreview: monthly UV")
print(uv_monthly.head())

print("\nPreview: hourly UV")
print(uv_hourly.head())

print("\nPreview: cancer trend")
print(cancer_chart.head())