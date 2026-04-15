import asyncio
import random
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://sgai:sgai_secret@localhost:5432/sgai"

ASSETS = [
  # Sucursales — Notebooks EXEC
  *[{"hostname":f"SUC-PROVIDENCIA-EXEC-{i:02d}","ip":f"10.50.1.{10+i}","cpu":"Intel Core i7-1365U","ram":"16 GB","disco":"250 GB","so":"Windows 11 Pro","tipo":"Notebook"} for i in range(1,9)],
  *[{"hostname":f"SUC-MAIPU-EXEC-{i:02d}","ip":f"10.50.2.{10+i}","cpu":"Intel Core i5-1335U","ram":"8 GB","disco":"180 GB","so":"Windows 11 Pro","tipo":"Notebook"} for i in range(1,7)],
  *[{"hostname":f"SUC-CONCE-EXEC-{i:02d}","ip":f"10.50.3.{10+i}","cpu":"Intel Core i5-1235U","ram":"8 GB","disco":"200 GB","so":"Windows 11 Pro","tipo":"Notebook"} for i in range(1,6)],
  # Sucursales — ATMs
  *[{"hostname":f"SUC-MAIPU-ATM-{i:02d}","ip":f"10.50.2.{50+i}","cpu":"Intel Atom E3940","ram":"4 GB","disco":"32 GB","so":"Embedded Windows 10 IoT","tipo":"Cajero"} for i in range(1,6)],
  *[{"hostname":f"SUC-PROVIDENCIA-ATM-{i:02d}","ip":f"10.50.1.{50+i}","cpu":"Intel Atom E3940","ram":"4 GB","disco":"32 GB","so":"Embedded Windows 10 IoT","tipo":"Cajero"} for i in range(1,5)],
  # Sucursales — Biométricos
  *[{"hostname":f"SUC-CONCE-BIOMET-{i:02d}","ip":f"10.50.3.{80+i}","cpu":"ARM Cortex-A53","ram":"1 GB","disco":"8 GB","so":"Embedded Linux","tipo":"Lector Huella"} for i in range(1,5)],
  *[{"hostname":f"SUC-MAIPU-BIOMET-{i:02d}","ip":f"10.50.2.{80+i}","cpu":"ARM Cortex-A53","ram":"1 GB","disco":"8 GB","so":"Embedded Linux","tipo":"Lector Huella"} for i in range(1,4)],
  # Casa Matriz — Servidores
  {"hostname":"CM-PISO4-SRV-CORE","ip":"10.50.0.10","cpu":"AMD EPYC 7443P","ram":"256 GB","disco":"2 TB","so":"Ubuntu Server 22.04","tipo":"Servidor"},
  {"hostname":"CM-PISO4-SRV-DB01","ip":"10.50.0.11","cpu":"AMD EPYC 7443P","ram":"128 GB","disco":"4 TB","so":"Ubuntu Server 22.04","tipo":"Servidor"},
  {"hostname":"CM-PISO4-SRV-APP01","ip":"10.50.0.12","cpu":"Intel Xeon Silver 4314","ram":"64 GB","disco":"1 TB","so":"Ubuntu Server 22.04","tipo":"Servidor"},
  {"hostname":"CM-PISO4-SRV-MON","ip":"10.50.0.13","cpu":"Intel Xeon Silver 4310","ram":"32 GB","disco":"500 GB","so":"Ubuntu Server 22.04","tipo":"Servidor"},
  # Casa Matriz — Workstations Dev
  {"hostname":"CM-PISO2-DEV-MAPAZA","ip":"10.50.0.50","cpu":"Intel Core i9-13900K","ram":"64 GB","disco":"1 TB","so":"Windows 11 Pro","tipo":"Workstation"},
  {"hostname":"CM-PISO2-DEV-SYSADM","ip":"10.50.0.51","cpu":"AMD Ryzen 9 7950X","ram":"64 GB","disco":"2 TB","so":"Ubuntu 22.04","tipo":"Workstation"},
  {"hostname":"CM-PISO2-DEV-DEVOPS","ip":"10.50.0.52","cpu":"Intel Core i7-13700K","ram":"32 GB","disco":"1 TB","so":"Ubuntu 22.04","tipo":"Workstation"},
  {"hostname":"CM-PISO2-DEV-SEGINFO","ip":"10.50.0.53","cpu":"Intel Core i7-12700","ram":"32 GB","disco":"512 GB","so":"Windows 11 Pro","tipo":"Workstation"},
  # Casa Matriz — Red
  {"hostname":"CM-BACKBONE-RTR-01","ip":"10.50.0.1","cpu":"Cisco IOS XE","ram":"8 GB","disco":"32 GB","so":"Embedded IOS","tipo":"Router"},
  {"hostname":"CM-BACKBONE-RTR-02","ip":"10.50.0.2","cpu":"Cisco IOS XE","ram":"8 GB","disco":"32 GB","so":"Embedded IOS","tipo":"Router"},
  {"hostname":"CM-PISO4-SW-CORE","ip":"10.50.0.3","cpu":"Embedded ASIC","ram":"4 GB","disco":"16 GB","so":"Embedded NX-OS","tipo":"Switch"},
]

async def seed():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(text("""
            ALTER TABLE assets ADD COLUMN IF NOT EXISTS so VARCHAR(100);
            ALTER TABLE assets ADD COLUMN IF NOT EXISTS tipo VARCHAR(100);
        """))

    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as db:
        now = datetime.now(timezone.utc)
        for a in ASSETS:
            delta = timedelta(minutes=random.randint(0, 120))
            ts = now - delta
            await db.execute(text("""
                INSERT INTO assets (hostname, ip_interna, modelo_cpu, ram_total, disco_libre, ultimo_reporte)
                VALUES (:hostname, :ip, :cpu, :ram, :disco, :ts)
                ON CONFLICT (hostname) DO UPDATE SET
                  ip_interna=EXCLUDED.ip_interna,
                  modelo_cpu=EXCLUDED.modelo_cpu,
                  ram_total=EXCLUDED.ram_total,
                  disco_libre=EXCLUDED.disco_libre,
                  ultimo_reporte=EXCLUDED.ultimo_reporte
            """), {"hostname":a["hostname"],"ip":a["ip"],"cpu":a["cpu"],
                   "ram":a["ram"],"disco":a["disco"],"ts":ts})
        await db.commit()
    await engine.dispose()
    print(f"✅ {len(ASSETS)} activos insertados")

asyncio.run(seed())
