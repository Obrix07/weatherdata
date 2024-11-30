from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuration de la connexion à PostgreSQL
DATABASE_URL = "postgresql://postgres:root@localhost:5432/weatherdata"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour récupérer une session de base de données
def get_db():
    """
    Génère une session de base de données SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
