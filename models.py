from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from database import Base

class CotacaoDB(Base):
    __tablename__ = "cotacoes"

    id = Column(Integer, primary_key=True, index=True)
    moeda = Column(String, index=True)
    valor = Column(Float)
    data_consulta = Column(DateTime, default=lambda: datetime.now(timezone.utc))