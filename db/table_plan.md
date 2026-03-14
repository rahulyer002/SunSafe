# Initial Table Plan

## Reference: Current project ER diagram

### 1. LOCATION
Fields:
- location_id (PK)
- latitude
- longitude
- city

Purpose:
Stores location details used to link UV data.

### 2. UV_CURRENT
Fields:
- uv_current_id (PK)
- location_id (FK)
- uv_index
- timestamp_current

Purpose:
Stores current UV readings for a location, likely from live API data.

### UV_HISTORICAL
Source:
- ARPANSA Melbourne UV data (2010–2024)

Processed file:
- data/processed/uv_historical_melbourne_all_years_clean.csv

Fields:
- date_time
- year
- month
- day
- hour
- minute
- latitude
- longitude
- uv_index
- city

Purpose:
Stores historical UV data for trend analysis and awareness features.

### 4. CANCER_INCIDENCE
Fields:
- cancer_id (PK)
- year
- sex
- age_group
- count
- incidence_rate
- icd10_code

Purpose:
Stores cancer incidence statistics for awareness visualisations.

## Notes
- This structure is based on the current ER diagram in the presentation.
- Final schema may still change depending on onboarding scope and feature updates.
- UV_CURRENT may remain partially API-driven rather than fully persisted.


