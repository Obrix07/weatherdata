from sqlalchemy import Column, BigInteger, Float, String, Date, Index, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

class GSODData(Base):
    __tablename__ = "gsod_data"

    STATION = Column(BigInteger, primary_key=True, index=True)
    DATE = Column(Date, nullable=False, index=True)
    LATITUDE = Column(Float, nullable=True)
    LONGITUDE = Column(Float, nullable=True)
    ELEVATION = Column(Float, nullable=True)
    NAME = Column(String, nullable=True)
    TEMP = Column(Float, nullable=True)
    TEMP_ATTRIBUTES = Column(Float, nullable=True)
    DEWP = Column(Float, nullable=True)
    DEWP_ATTRIBUTES = Column(Float, nullable=True)
    SLP = Column(Float, nullable=True)
    SLP_ATTRIBUTES = Column(Float, nullable=True)
    STP = Column(Float, nullable=True)
    STP_ATTRIBUTES = Column(Float, nullable=True)
    VISIB = Column(Float, nullable=True)
    VISIB_ATTRIBUTES = Column(Float, nullable=True)
    WDSP = Column(Float, nullable=True)
    WDSP_ATTRIBUTES = Column(Float, nullable=True)
    MXSPD = Column(Float, nullable=True)
    GUST = Column(Float, nullable=True)
    MAX = Column(Float, nullable=True)
    MAX_ATTRIBUTES = Column(String, nullable=True)
    MIN = Column(Float, nullable=True)
    MIN_ATTRIBUTES = Column(String, nullable=True)
    PRCP = Column(Float, nullable=True)
    PRCP_ATTRIBUTES = Column(String, nullable=True)
    SNDP = Column(Float, nullable=True)
    FRSHTT = Column(BigInteger, nullable=True)


    __table_args__ = (
        Index("idx_station", "STATION"),
        Index("idx_date", "DATE"),
        Index("idx_station_date", "STATION", "DATE"),
    )