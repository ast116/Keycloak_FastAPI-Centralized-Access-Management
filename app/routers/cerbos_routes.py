from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.Cerbos.audit_services import get_audits_grouped_by_resource, get_audits_by_user, get_audits_by_date, get_audits_by_date_range
from app.models.cerbos import DateRange

router = APIRouter(prefix="/audits", tags=["Cerbos Audits"])

@router.get("/resources")
def audits_resources():
    try:
        return get_audits_grouped_by_resource()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/user/{user_id}")
def audits_for_user(user_id: str):
    try:
        return get_audits_by_user(user_id)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/date/{date}")
def audits_for_date(date: str):
    try:
        return get_audits_by_date(date)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/date-range")
def audits_range(payload: DateRange):
    try:
        return get_audits_by_date_range(payload.start, payload.end)
    except Exception as e:
        raise HTTPException(500, str(e))
