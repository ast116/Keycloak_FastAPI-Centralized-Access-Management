import requests
from typing import Optional, Dict, Any
from app.config import (
    CERBOS_ADMIN_URL,
    CERBOS_ADMIN_USERNAME,
    CERBOS_ADMIN_PASSWORD
)


def cerbos_admin_get(path: str, params: Optional[Dict[str, Any]] = None):
   
    url = f"{CERBOS_ADMIN_URL}{path}"

    response = requests.get(
        url,
        params=params,
        auth=(CERBOS_ADMIN_USERNAME, CERBOS_ADMIN_PASSWORD)
    )

    if response.status_code != 200:
        raise Exception(f"Erreur API Cerbos: {response.status_code} - {response.text}")

    return response.json()


# ====================
# AUDIT SERVICES
# ====================

def get_audits_grouped_by_resource():
    return cerbos_admin_get("/auditlog", {"groupBy": "resource"})


def get_audits_by_user(user_id: str):
    return cerbos_admin_get("/auditlog", {"user": user_id})


def get_audits_by_date(date: str):
    return cerbos_admin_get("/auditlog", {"date": date})


def get_audits_by_date_range(start: str, end: str):
    return cerbos_admin_get("/auditlog", {"start": start, "end": end})
