"""IngeInv — FastAPI application entry point.

Run with:
    uvicorn src.ingeinv.main:app --reload
"""
from fastapi import FastAPI
from src.ingeinv.database import create_tables
from src.ingeinv.routers import machines, maintenance, predictions

app = FastAPI(
    title="IngeInv",
    description=(
        "Plataforma de gestión inteligente de mantenimiento industrial. "
        "Gestiona máquinas, componentes, lecturas de sensores y predice fallos "
        "con ayuda de inteligencia artificial."
    ),
    version="0.1.0",
)

# Ensure all tables exist at startup
create_tables()

app.include_router(machines.router)
app.include_router(maintenance.router)
app.include_router(predictions.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "app": "IngeInv", "version": "0.1.0"}
