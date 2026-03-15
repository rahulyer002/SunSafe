import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

print("Connected to PostgreSQL")

with engine.connect() as conn:

    conn.execute(text("DROP TABLE IF EXISTS heat_trend"))
    conn.execute(text("DROP TABLE IF EXISTS skin_profile"))
    conn.execute(text("DROP TABLE IF EXISTS cancer_incidence"))

    conn.execute(text("""
        CREATE TABLE heat_trend (
            id SERIAL PRIMARY KEY,
            year INTEGER,
            uv_index FLOAT,
            city TEXT
        )
    """))

    conn.execute(text("""
        CREATE TABLE skin_profile (
            id SERIAL PRIMARY KEY,
            skin_tone TEXT,
            uv_index_min FLOAT,
            uv_index_max FLOAT,
            predicted_damage TEXT
        )
    """))

    conn.execute(text("""
        CREATE TABLE cancer_incidence (
            id SERIAL PRIMARY KEY,
            year INTEGER,
            incidence_rate FLOAT,
            city TEXT
        )
    """))

    conn.commit()

print("Tables recreated")


heat_df = pd.read_csv("data/processed/chart_uv_monthly_avg.csv")

heat_df["city"] = "Melbourne"
heat_df = heat_df.rename(columns={"avg_uv_index": "uv_index"})
heat_df = heat_df[["year", "uv_index", "city"]]

heat_df.to_sql("heat_trend", engine, if_exists="append", index=False)

print("Heat trend data inserted")


skin_df = pd.read_csv("data/processed/uv_skin_profile_lookup.csv")

skin_df = skin_df.rename(
    columns={"predicted_damage_accumulation": "predicted_damage"}
)

skin_df = skin_df[
    ["skin_tone", "uv_index_min", "uv_index_max", "predicted_damage"]
]

skin_df.to_sql("skin_profile", engine, if_exists="append", index=False)

print("Skin profile data inserted")


cancer_df = pd.read_csv("data/processed/chart_skin_cancer_trend.csv")

cancer_df = cancer_df[
    ["year", "incidence_rate", "city"]
]

cancer_df.to_sql("cancer_incidence", engine, if_exists="append", index=False)

print("Cancer incidence data inserted")

print("All datasets inserted successfully")