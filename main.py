# coding=utf-8
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import diagnosticos, enfermeros
import uvicorn

# Crear tablas en la DB
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NandaDiagnosticosAPI",
    version="2.0.0",
    description="API REST Profesional - Diagnósticos NANDA"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(diagnosticos.router)
app.include_router(enfermeros.router)

@app.get("/", tags=["Info"])
async def root():
    return {
        "mensaje": "API de Diagnósticos NANDA Online ✅",
        "docs": "/docs",
        "rutas": "/diagnosticos"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)