import pandas as pd

output_file = "data/processed/uv_skin_profile_lookup.csv"

rows = [
    # Fair skin
    {"skin_tone": "Fair", "uv_index_min": 0, "uv_index_max": 2, "risk_level": "Low", "predicted_damage_accumulation": "Low",              "recommended_action": "Minimal protection needed"},
    {"skin_tone": "Fair", "uv_index_min": 3, "uv_index_max": 5, "risk_level": "Moderate", "predicted_damage_accumulation": "Moderate",         "recommended_action": "Use sunscreen and sunglasses"},
    {"skin_tone": "Fair", "uv_index_min": 6, "uv_index_max": 7, "risk_level": "High", "predicted_damage_accumulation": "High",             "recommended_action": "Limit exposure and seek shade"},
    {"skin_tone": "Fair", "uv_index_min": 8, "uv_index_max": 10, "risk_level": "Very High", "predicted_damage_accumulation": "Very High",        "recommended_action": "Avoid prolonged sun exposure"},
    {"skin_tone": "Fair", "uv_index_min": 11, "uv_index_max": 20, "risk_level": "Extreme", "predicted_damage_accumulation": "Extreme",          "recommended_action": "Minimise sun exposure immediately"},

    # Medium skin
    {"skin_tone": "Medium", "uv_index_min": 0, "uv_index_max": 2, "risk_level": "Low", "predicted_damage_accumulation": "Low",              "recommended_action": "Minimal protection needed"},
    {"skin_tone": "Medium", "uv_index_min": 3, "uv_index_max": 5, "risk_level": "Moderate", "predicted_damage_accumulation": "Low to Moderate",  "recommended_action": "Use sunscreen if outdoors"},
    {"skin_tone": "Medium", "uv_index_min": 6, "uv_index_max": 7, "risk_level": "High", "predicted_damage_accumulation": "Moderate",         "recommended_action": "Seek shade during peak UV"},
    {"skin_tone": "Medium", "uv_index_min": 8, "uv_index_max": 10, "risk_level": "Very High", "predicted_damage_accumulation": "High",             "recommended_action": "Use strong protection"},
    {"skin_tone": "Medium", "uv_index_min": 11, "uv_index_max": 20, "risk_level": "Extreme", "predicted_damage_accumulation": "Very High",        "recommended_action": "Avoid prolonged exposure"},

    # Dark skin
    {"skin_tone": "Dark", "uv_index_min": 0, "uv_index_max": 2, "risk_level": "Low", "predicted_damage_accumulation": "Very Low",         "recommended_action": "Minimal protection needed"},
    {"skin_tone": "Dark", "uv_index_min": 3, "uv_index_max": 5, "risk_level": "Moderate", "predicted_damage_accumulation": "Low",              "recommended_action": "Protection still recommended"},
    {"skin_tone": "Dark", "uv_index_min": 6, "uv_index_max": 7, "risk_level": "High", "predicted_damage_accumulation": "Moderate",         "recommended_action": "Use sunscreen and limit exposure"},
    {"skin_tone": "Dark", "uv_index_min": 8, "uv_index_max": 10, "risk_level": "Very High", "predicted_damage_accumulation": "High",             "recommended_action": "Strong protection recommended"},
    {"skin_tone": "Dark", "uv_index_min": 11, "uv_index_max": 20, "risk_level": "Extreme", "predicted_damage_accumulation": "Very High",        "recommended_action": "Avoid prolonged exposure"},
]

df = pd.DataFrame(rows)
df.to_csv(output_file, index=False)

print("Saved UV skin profile lookup to:")
print(output_file)

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nPreview:")
print(df.head(15))