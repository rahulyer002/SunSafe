from sqlalchemy import text
from app.database import engine

def get_skin_profiles():
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT skin_tone, uv_index_min, uv_index_max, predicted_damage FROM skin_profile"
            )
        )
        rows = [dict(row._mapping) for row in result]
        return rows
    