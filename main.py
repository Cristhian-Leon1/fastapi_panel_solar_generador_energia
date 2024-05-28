import uvicorn
from fastapi import FastAPI
from backend.routes.rutas_generador import get_router
from backend.mongoDB.conexion_mongo import establecer_conexion
from fastapi.middleware.cors import CORSMiddleware

variables_collection = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


def start_application():
    global variables_collection
    variables_collection = establecer_conexion()
    app.include_router(get_router(variables_collection), prefix="/api")


if __name__ == "__main__":
    start_application()
    uvicorn.run(app, host="0.0.0.0", port=10000)
