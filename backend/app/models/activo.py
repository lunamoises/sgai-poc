from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase): pass
class Activo(Base):
    __tablename__ = "activos"
    id         = Column(Integer, primary_key=True)
    nombre     = Column(String(200), nullable=False)
    codigo     = Column(String(50), unique=True, nullable=False)
    categoria  = Column(String(100))
    estado     = Column(String(50), default="activo")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
