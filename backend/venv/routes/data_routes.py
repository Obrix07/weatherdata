from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from sqlalchemy import select
from database import get_db
from models import GSODData
from fastapi import Query

router = APIRouter()

@router.get("/sample")
def get_sample_data(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Récupère un échantillon des données depuis la table gsod_data (1 ligne).
    """
    try:
        stmt = select(GSODData).limit(1)
        result = db.scalars(stmt).first()

        if not result:
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée dans la table gsod_data.")

        return {"data": result.__dict__}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données : {e}")


@router.get("/all")
def get_all_data_with_pagination(db: Session = Depends(get_db), limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0), user=Depends(get_current_user)):
    """
    Récupère les données depuis la table gsod_data avec pagination.
    """
    try:
        total_count = db.query(GSODData).count()

        stmt = select(GSODData).limit(limit).offset(offset)
        results = db.scalars(stmt).all()

        if not results:
            raise HTTPException(status_code=404, detail="Aucune donnée trouvée dans la table gsod_data.")

        return {
            "data": [result.__dict__ for result in results],
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": offset
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données : {e}")



@router.get("/by-station/{station_id}")
def get_data_by_station(station_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Récupère toutes les données pour une station spécifique.
    """
    try:
        stmt = select(GSODData).where(GSODData.STATION == station_id)
        results = db.scalars(stmt).all()

        if not results:
            raise HTTPException(status_code=404, detail=f"Aucune donnée trouvée pour la station {station_id}.")

        return {"data": [result.__dict__ for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données pour la station {station_id} : {e}")

@router.get("/max-temperature")
def get_max_temperature_by_station(
    station_name: str = Query(..., description="Nom de la station"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Récupère les températures maximales par date pour une station donnée.
    """
    try:
        results = (
            db.query(GSODData.DATE, GSODData.MAX)
            .filter(GSODData.NAME == station_name)
            .order_by(GSODData.DATE.asc())
            .all()
        )

        if not results:
            raise HTTPException(status_code=404, detail=f"Aucune donnée trouvée pour la station '{station_name}'.")

        return [{"date": row.DATE, "max_temperature": row.MAX} for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données : {e}")


@router.get("/stations")
def get_all_stations(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Récupère tous les noms de stations distincts.
    """
    try:
        stations = db.query(GSODData.NAME).distinct().all()
        return {"stations": [station[0] for station in stations]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des stations : {e}")