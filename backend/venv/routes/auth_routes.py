from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from auth import create_access_token, verify_password, hash_password, get_current_user
from database import get_db
from models import User

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.get("/validate-token")
def validate_token(user=Depends(get_current_user)):
    """
    Valide le token JWT de l'utilisateur.
    """
    return {"message": "Token is valid"}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authentifie un utilisateur et retourne un token JWT.
    """
    # Rechercher l'utilisateur dans la base de données
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect.")
    
    # Générer un token JWT
    access_token = create_access_token(data={"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Enregistre un nouvel utilisateur.
    """
    # Vérifier si le nom d'utilisateur existe déjà
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé.")
    
    # Hacher le mot de passe
    hashed_password = hash_password(request.password)

    # Créer un nouvel utilisateur
    new_user = User(username=request.username, hashed_password=hashed_password, is_admin=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Utilisateur créé avec succès."}
