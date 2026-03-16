# import pandas as pd

# # input/output paths
# input_file = "data/raw/arpansa_melbourne_2024_raw.csv"
# output_file = "data/processed/uv_historical_melbourne_2024_clean.csv"

# # read raw data
# df = pd.read_csv(input_file)

# # rename columns
# df = df.rename(columns={
#     "Date-Time": "date_time",
#     "Lat": "latitude",
#     "Lon": "longitude",
#     "UV_Index": "uv_index"
# })

# # convert datetime
# df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")

# # create time breakdown columns
# df["year"] = df["date_time"].dt.year
# df["month"] = df["date_time"].dt.month
# df["day"] = df["date_time"].dt.day
# df["hour"] = df["date_time"].dt.hour
# df["minute"] = df["date_time"].dt.minute

# # add city
# df["city"] = "Melbourne"

# # reorder columns
# df = df[
#     [
#         "date_time",
#         "year",
#         "month",
#         "day",
#         "hour",
#         "minute",
#         "latitude",
#         "longitude",
#         "uv_index",
#         "city"
#     ]
# ]

# # save cleaned file
# df.to_csv(output_file, index=False)

# print("Saved cleaned file to:")
# print(output_file)

# print("\nShape:")
# print(df.shape)

# print("\nColumns:")
# print(df.columns.tolist())

# print("\nFirst 5 rows:")
# print(df.head())



######


import pandas as pd
import glob

# Find all Melbourne ARPANSA raw files
arpansa_files = sorted(glob.glob("data/raw/arpansa_melbourne_*_raw.csv"))

all_dfs = []

for file in arpansa_files:
    print(f"\nProcessing: {file}")

    # Read raw CSV
    df = pd.read_csv(file)

    # Clean column names first
    df.columns = df.columns.str.strip()

    # Rename possible header variants into one standard format
    df = df.rename(columns={
        "Date-Time": "date_time",
        "DateTime": "date_time",
        "date_time": "date_time",
        "Date Time": "date_time",
        "timestamp": "date_time",

        "Lat": "latitude",
        "Latitude": "latitude",
        "latitude": "latitude",

        "Lon": "longitude",
        "Longitude": "longitude",
        "longitude": "longitude",

        "UV_Index": "uv_index",
        "UV Index": "uv_index",
        "uv_index": "uv_index"
    })

    # Check whether required columns exist
    required_cols = ["date_time", "latitude", "longitude", "uv_index"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        print(f"Skipping {file}")
        print("Missing columns:", missing_cols)
        print("Actual columns:", df.columns.tolist())
        continue

    # Convert datetime
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")

    # Add helpful time breakdown columns
    df["year"] = df["date_time"].dt.year
    df["month"] = df["date_time"].dt.month
    df["day"] = df["date_time"].dt.day
    df["hour"] = df["date_time"].dt.hour
    df["minute"] = df["date_time"].dt.minute

    # Add city
    df["city"] = "Melbourne"

    # Keep columns in a clean backend-friendly order
    df = df[
        [
            "date_time",
            "year",
            "month",
            "day",
            "hour",
            "minute",
            "latitude",
            "longitude",
            "uv_index",
            "city"
        ]
    ]

    all_dfs.append(df)

# Check whether any files were successfully processed
if not all_dfs:
    print("\nNo ARPANSA files were processed successfully.")
else:
    # Combine all years
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Sort by datetime
    combined_df = combined_df.sort_values("date_time").reset_index(drop=True)

    # Save final combined file
    output_file = "data/processed/uv_historical_melbourne_all_years_clean.csv"
    combined_df.to_csv(output_file, index=False)

    print("\nSaved combined file to:")
    print(output_file)

    print("\nFinal shape:")
    print(combined_df.shape)

    print("\nColumns:")
    print(combined_df.columns.tolist())

    print("\nFirst 5 rows:")
    print(combined_df.head())

    print("\nLast 5 rows:")
    print(combined_df.tail())


