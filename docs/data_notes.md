## Current proposed data sources

1. OpenWeather API - real-time UV data (https://openweathermap.org/api/one-call-3?collection=one_call_api_3.0)
2. ARPANSA - historical UV data (https://data.gov.au/data/organization/australian-radiation-protection-and-nuclear-safety-agency-arpansa)
3. AIHW - skin cancer incidence data (https://www.aihw.gov.au/getmedia/e8779760-1b3c-4c2e-a6c2-b0a8d764c66b/AIHW-CAN-122-CDiA-2021-Book-1a-Cancer-incidence-age-standardised-rates-5-year-age-groups.xlsx.aspx)

## Mapping to current ER diagram

- OpenWeather API -> UV_CURRENT
- ARPANSA -> UV_HISTORICAL
- AIHW -> CANCER_INCIDENCE
- Location data -> LOCATION

## Current assumptions
- OpenWeather will be used for live UV checks
- ARPANSA historical UV data will be cleaned into the UV_HISTORICAL table
- AIHW cancer incidence data will be cleaned into the CANCER_INCIDENCE table
- LOCATION will support linking UV data by city or coordinates
- Final schema may change once onboarding scope is fully confirmed


## ARPANSA processing status

- Raw Melbourne UV files from 2010 to 2024 were combined successfully
- Output file: data/processed/uv_historical_melbourne_all_years_clean.csv
- Final fields:
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
- City is currently fixed as Melbourne

** Note: uv_historical_melbourne_2024_clean.csv in the processed folder is a test case for checking the pipeline on only the 2024 data