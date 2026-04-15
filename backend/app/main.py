from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Column, Integer, String, Boolean, DateTime, func, text
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.database import get_db, engine

API_KEY = "sgai-secret-key-2026"

app = FastAPI(title="SGAI API v2")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Base(DeclarativeBase): pass

class Asset(Base):
    __tablename__ = "assets"
    id             = Column(Integer, primary_key=True)
    hostname       = Column(String(200), nullable=False)
    ip_interna     = Column(String(50))
    modelo_cpu     = Column(String(200))
    ram_total      = Column(String(50))
    disco_libre    = Column(String(50))
    so_operativo   = Column(String(100))
    vulnerabilidad = Column(Boolean, default=False)
    ultimo_reporte = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class AssetIn(BaseModel):
    hostname: str
    ip_interna: Optional[str] = None
    modelo_cpu: Optional[str] = None
    ram_total: Optional[str] = None
    disco_libre: Optional[str] = None
    so_operativo: Optional[str] = None
    vulnerabilidad: Optional[bool] = False

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Migraciones no destructivas: añade columnas nuevas si no existen
        await conn.execute(text(
            "ALTER TABLE assets ADD COLUMN IF NOT EXISTS so_operativo VARCHAR(100);"
        ))
        await conn.execute(text(
            "ALTER TABLE assets ADD COLUMN IF NOT EXISTS vulnerabilidad BOOLEAN DEFAULT FALSE;"
        ))

def verify_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")
    return x_api_key

@app.post("/v1/assets/register", status_code=201)
async def register_asset(payload: AssetIn, db: AsyncSession = Depends(get_db), key: str = Depends(verify_key)):
    result = await db.execute(select(Asset).where(Asset.hostname == payload.hostname))
    obj = result.scalar_one_or_none()
    if obj:
        for k, v in payload.model_dump().items():
            setattr(obj, k, v)
        obj.ultimo_reporte = func.now()
    else:
        obj = Asset(**payload.model_dump())
        db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

@app.get("/v1/assets")
async def list_assets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Asset))
    return result.scalars().all()

@app.get("/health")
async def health(): return {"status": "ok"}
