from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.activo import Activo
from app.schemas.activo import ActivoCreate, ActivoOut
router = APIRouter(tags=["activos"])
@router.get("/activos", response_model=list[ActivoOut])
async def list_activos(db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Activo))).scalars().all()
@router.get("/activos/{activo_id}", response_model=ActivoOut)
async def get_activo(activo_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Activo, activo_id)
    if not obj: raise HTTPException(404, "No encontrado")
    return obj
@router.post("/activos", response_model=ActivoOut, status_code=201)
async def create_activo(payload: ActivoCreate, db: AsyncSession = Depends(get_db)):
    obj = Activo(**payload.model_dump()); db.add(obj); await db.commit(); await db.refresh(obj); return obj
