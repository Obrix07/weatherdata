from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.data_routes import router as data_router
from routes.analysis_routes import router as analysis_router
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Weather Data API",
    description="API pour accéder et analyser les données météorologiques NOAA",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(data_router, prefix="/api/data", tags=["Data"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["Analysis"])

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Weather Data"}

for route in app.router.routes:
    print(f"Route enregistrée : {route.path}")


# Configurer le logger
logging.basicConfig(
    filename='debug.log',  # Nom du fichier de log
    level=logging.DEBUG,  # Niveau des logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

# Liste des origines autorisées
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser les origines spécifiées
    allow_credentials=True,  # Autoriser l'envoi de cookies ou d'en-têtes d'authentification
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les en-têtes
)