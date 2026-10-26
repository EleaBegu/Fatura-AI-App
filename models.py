from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# 1. Tabela për artikujt e depos (Shtrafa, vegla, pajisje)
class Produkti(Base):
    __tablename__ = "produktet"

    id = Column(Integer, primary_key=True, index=True)
    kodi = Column(String, unique=True, index=True)
    emri = Column(String, nullable=False)
    kategoria = Column(String, nullable=True)
    njesia = Column(String, default="copë")
    cmimi = Column(Float, default=0.0)

# 2. Tabela kryesore e faturës
class Fatura(Base):
    __tablename__ = "faturat"

    id = Column(Integer, primary_key=True, index=True)
    nr_fatures = Column(String, index=True)
    furnizuesi = Column(String, nullable=True)
    shuma_totale = Column(Float, default=0.0)
    tvsh = Column(Float, default=0.0)
    data_fatures = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    rreshtat = relationship("RreshtiFatures", back_populates="fatura")

# 3. Artikujt brenda faturës
class RreshtiFatures(Base):
    __tablename__ = "rreshtat_fatures"

    id = Column(Integer, primary_key=True, index=True)
    fatura_id = Column(Integer, ForeignKey("faturat.id"))
    pershkrimi = Column(String, nullable=False)
    sasia = Column(Float, default=1.0)
    cmimi_njesi = Column(Float, default=0.0)
    nentotali = Column(Float, default=0.0)

    fatura = relationship("Fatura", back_populates="rreshtat")
    