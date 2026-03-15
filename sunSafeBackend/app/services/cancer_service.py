from sqlalchemy import text
from app.database import engine

def get_cancer_incidence():
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT year, incidence_rate, city FROM cancer_incidence ORDER BY year"
            )
        )
        rows = [dict(row._mapping) for row in result]
        return rows
    
