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

### 3. UV_HISTORICAL
Fields:
- uv_hist_id (PK)
- location_id (FK)
- date_time
- uv_index

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