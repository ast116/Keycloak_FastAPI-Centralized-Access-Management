from fastapi.responses import StreamingResponse
from app.admin.admin_client import keycloak_admin_request
from typing import Optional
from datetime import datetime
import csv
import io
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse

def list_events(event_type: Optional[str] = None, user: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None):
    """
    Récupère les logs d'événements depuis Keycloak avec filtres possibles.
    
    - event_type : type d'événement (LOGIN, LOGOUT, CREATE, UPDATE, DELETE, etc.)
    - user       : id de l'utilisateur
    - from_date  : date début au format 'YYYY-MM-DDTHH:MM:SS'
    - to_date    : date fin au format 'YYYY-MM-DDTHH:MM:SS'
    """
    params = {}
    if event_type:
        params["type"] = event_type
    if user:
        params["user"] = user
    if from_date:
        params["dateFrom"] = from_date
    if to_date:
        params["dateTo"] = to_date

    endpoint = "events"
    return keycloak_admin_request("GET", endpoint, params=params)



def export_events_csv(event_type: Optional[str] = None, user: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None):
    """
    Exporte les logs d'événements depuis Keycloak au format CSV.
    """
    # Récupération des logs
    params = {}
    if event_type:
        params["type"] = event_type
    if user:
        params["user"] = user
    if from_date:
        params["dateFrom"] = from_date
    if to_date:
        params["dateTo"] = to_date

    logs = keycloak_admin_request("GET", "events", params=params)
    if logs is None:
        logs = []

    # Création du CSV en mémoire
    output = io.StringIO()
    writer = csv.writer(output)

    # Entête
    writer.writerow(["Event ID", "Type", "User ID", "Username", "Date", "IP", "Details"])

    for log in logs:
        writer.writerow([
            log.get("id"),
            log.get("type"),
            log.get("userId"),
            log.get("username"),
            log.get("time"),
            log.get("ipAddress"),
            log.get("details")
        ])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=keycloak_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
    )

