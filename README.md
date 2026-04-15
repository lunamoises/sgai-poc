# SGAI v2 — Sistema de Gestión de Activos Institucionales

## Stack
| Servicio   | Imagen              | Puerto externo |
|------------|---------------------|----------------|
| KrakenD    | devopsfaith/krakend | 80             |
| FastAPI    | python:3.12-slim    | interno        |
| PostgreSQL | postgres:15-alpine  | interno        |
| React/Vite | nginx:alpine        | 3000           |

## Inicio rápido
```bash
git clone https://github.com/lunamoises/sgai-poc
cd sgai-poc
docker compose up --build -d
```

## Endpoints
| Método | URL | Auth |
|--------|-----|------|
| POST | http://SERVER/v1/register | X-API-KEY header |
| GET  | http://SERVER/v1/assets   | ninguna |

## Agente Windows
```powershell
.\agent.ps1 -ServerIP 192.168.100.152 -ApiKey sgai-secret-key-2026
```

## Dashboard
http://192.168.100.152:3000
- 🟢 Verde: reporte hace < 5 minutos
- 🔴 Rojo: sin reporte reciente
