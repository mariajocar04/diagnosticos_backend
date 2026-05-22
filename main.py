# coding=utf-8
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, diagnosticos, pacientes, reportes, admin, remisiones

app = FastAPI(
    title="TICOS NurseDx API",
    version="2.0.0",
    description="API REST Profesional - Diagnósticos NANDA (MVP)"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefijo global para la API v1
api_v1_prefix = "/api/v1"

# Incluir los routers
app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(diagnosticos.router, prefix=api_v1_prefix)
app.include_router(pacientes.router, prefix=api_v1_prefix)
app.include_router(reportes.router, prefix=api_v1_prefix, tags=["Reportes"])
app.include_router(admin.router, prefix=api_v1_prefix, tags=["Administración"])
app.include_router(remisiones.router, prefix=api_v1_prefix, tags=["Remisiones"])

@app.get("/", tags=["Info"])
async def root():
    return {
        "mensaje": "TICOS NurseDx API Online ✅",
        "docs": "/docs",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)