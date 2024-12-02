from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import GSODData

router = APIRouter()

@router.get("/average-temperature")
def get_average_temperature(db: Session = Depends(get_db)):
    """
    Calcule la température moyenne par année.
    """
    try:
        results = (
            db.query(
                func.extract('year', GSODData.DATE).label('year'),
                func.avg(GSODData.TEMP).label('average_temperature')
            )
            .group_by('year')
            .order_by('year')
            .all()
        )
        return [
            {"year": int(result.year), "average_temperature": result.average_temperature}
            for result in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse : {e}")


@router.get("/total-precipitation")
def get_total_precipitation(db: Session = Depends(get_db)):
    """
    Calcule les précipitations totales par année.
    """
    try:
        results = (
            db.query(
                func.extract('year', GSODData.DATE).label('year'),
                func.sum(GSODData.PRCP).label('total_precipitation')
            )
            .group_by('year')
            .order_by('year')
            .all()
        )
        return [
            {"year": int(result.year), "total_precipitation": result.total_precipitation}
            for result in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse : {e}")


@router.get("/hottest-days")
def get_hottest_days(limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupère les jours les plus chauds.
    """
    try:
        results = (
            db.query(
                GSODData.DATE,
                func.max(GSODData.TEMP).label('max_temperature')
            )
            .group_by(GSODData.DATE)
            .order_by(func.max(GSODData.TEMP).desc())
            .limit(limit)
            .all()
        )
        return [
            {"date": result.DATE, "max_temperature": result.max_temperature}
            for result in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse : {e}")
