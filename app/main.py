from fastapi import FastAPI
from app.routers import protected, admin_routes

app = FastAPI(title="FastAPI + Keycloak Auth")

# Inclure les routes
app.include_router(protected.router, prefix="/api", tags=["Protected"])
app.include_router(admin_routes.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Gateway sécurisée par Keycloak"}
