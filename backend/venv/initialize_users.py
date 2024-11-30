from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, User
from auth import hash_password

def initialize_admin_user():
    """Crée un utilisateur administrateur si aucun utilisateur n'existe."""
    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Vérifiez s'il existe déjà des utilisateurs
        user_count = db.query(User).count()
        if user_count == 0:
            # Créez un utilisateur admin par défaut
            admin = User(
                username="admin",
                hashed_password=hash_password("admin123"),
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("Administrateur créé : admin / admin123")
        else:
            print("Des utilisateurs existent déjà. Aucun administrateur ajouté.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    initialize_admin_user()
