from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, Text

Base = declarative_base()


class HeatTrend(Base):
    __tablename__ = "heat_trend"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    uv_index = Column(Float)
    city = Column(Text)


class SkinProfile(Base):
    __tablename__ = "skin_profile"

    id = Column(Integer, primary_key=True)
    skin_tone = Column(Text)
    uv_index_min = Column(Float)
    uv_index_max = Column(Float)
    predicted_damage = Column(Text)


class CancerIncidence(Base):
    __tablename__ = "cancer_incidence"

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    incidence_rate = Column(Float)
    city = Column(Text)