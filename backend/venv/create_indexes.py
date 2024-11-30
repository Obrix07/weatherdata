from sqlalchemy import create_engine
from models import Base
from database import engine

if __name__ == "__main__":
    # Connexion à la base de données
    print("Création des index pour la base de données...")

    # Appliquer les index définis dans les modèles
    Base.metadata.create_all(bind=engine)

    print("Les index ont été créés avec succès.")
