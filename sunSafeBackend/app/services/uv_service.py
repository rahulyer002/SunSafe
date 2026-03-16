from sqlalchemy import text
from app.database import engine

def get_uv_trend():
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT year, uv_index, city FROM heat_trend ORDER BY year"
            )
        )
        rows = [dict(row._mapping) for row in result]
        return rows
    