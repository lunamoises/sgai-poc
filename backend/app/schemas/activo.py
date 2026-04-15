from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class ActivoBase(BaseModel):
    nombre: str; codigo: str; categoria: Optional[str]=None; estado: str="activo"
class ActivoCreate(ActivoBase): pass
class ActivoOut(ActivoBase):
    id: int; created_at: datetime
    class Config: from_attributes=True
