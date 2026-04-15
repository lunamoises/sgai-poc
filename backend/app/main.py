from fastapi import FastAPI
from app.api.v1.endpoints import activos
app = FastAPI(title="SGAI API")
app.include_router(activos.router, prefix="/api/v1")
@app.get("/health")
async def health(): return {"status":"ok"}
