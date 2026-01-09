# Fabrica Perobell

Aplicación PWA para la gestión completa de fabricación de sofás: modelos, módulos, escandallo, stock, proveedores, compras, producción y pedidos.

## Estructura

- `backend/`: API en FastAPI + SQLModel.
- `frontend/`: PWA en React + Vite.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

La PWA consume la API en `http://localhost:8000/api` (configurable con `VITE_API_BASE`).
