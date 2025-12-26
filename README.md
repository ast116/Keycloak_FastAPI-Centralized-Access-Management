# FastAPI Keycloak Admin Backend

Un backend FastAPI complet pour gérer l'authentification OAuth2/OpenID Connect via Keycloak, avec API REST pour la gestion des utilisateurs, rôles, et fournisseurs d'identité.

## Architecture

```
fastapi-project/
├── main.py         # Point d'entrée de l'application
├── config.py       # Configuration Keycloak                 
├── app/             
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                  # Modèles utilisateur
│   │   ├── realm.py                 # Modèles realm
│   │   └── identity_provider.py      # Modèles fournisseur d'identité
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── user_management.py        # Gestion des utilisateurs
│   │   ├── role_management.py        # Gestion des rôles
│   │   └── realm_management.py       # Gestion des realms
│   └── routers/
│       ├── __init__.py
│       └── admin_routes.py            # Endpoints API
|       └── auth_route.py             #Endpoint obtention Token utilisateur
├── requirements.txt
└── README.md
```

## Variables d'environnement

Dans config.py remplacer les points suivant votre configuration keycloak :

```
# Configuration Keycloak (Creer deux clients dans un realms avec deux noms differents(fastapi-gateway/fastapi-admin))

KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=master
KEYCLOAK_CLIENT_ID=admin-cli        #fastapi-gateway par exemple comme nom
KEYCLOAK_CLIENT_SECRET=your-client-secret
KEYCLOAK_ADMIN_CLIENT_ID=admin-cli  #fastapi-admin par exemple comme nom
KEYCLOAK_ADMIN_CLIENT_SECRET=your-admin-client-secret

## Dans le fichier admin_master.py dans le dossier admin remplacer les champs suivant :

username=admin # Username du master de keycloak
password=admin # Password du master de keycloak

# Configuration FastAPI
FASTAPI_ENV=development
DEBUG=True
```

## Configuration des deux Clients

Creer d'abord un realm (exemple : myrealm), ensuite creer deux clients dans le realm

### Client (fastapi-gateway/fastapi-admin)

Dans setting de fastapi-gateway activer:
    
    Client authentication
    Authorization
    Standard Flow
    Direct access grants

Dans setting de fastapi-admin activer:

    Client authentication
    Authorization
    Standard Flow
    Direct access grants

Toujours dans fastapi-admin allez dans le menu Service account role, assigner les roles suivant : 

    realm-management               manage-realm
    realm-management               view-realm
    realm-management               realm-admin
    realm-management               manage-identity-providers

Maintenant sortez et aller dans le realm master de keycloak, ensuite user, menu Role mapping, assigner le role suivant : 

    admin

Cree un utilisateur dans le realm crée (myrealm et non dans realm master)

    username=test # exemple de nom
    credential=test # exemple de mot de passe

## Installation et Exécution

### Prérequis

- Python 3.9+
- Keycloak en exécution sur `http://localhost:8080`

### Étapes d'installation

1. **Cloner le dépôt**

```bash
cd /home/ast116/fastapi-project
```

2. **Créer un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**


5. **Lancer l'application**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur `http://localhost:8000`

## Endpoints API

### Gestion des Utilisateurs

- `POST /admin/users` - Créer un utilisateur
- `GET /admin/users/{user_id}` - Récupérer un utilisateur
- `PUT /admin/users/{user_id}` - Mettre à jour un utilisateur
- `DELETE /admin/users/{user_id}` - Supprimer un utilisateur
- `POST /admin/users/{user_id}/reset-password` - Réinitialiser le mot de passe

### Gestion des Rôles

- `POST /admin/roles/client` - Créer un rôle client
- `GET /admin/roles/client/{client_id}` - Lister les rôles d'un client
- `PUT /admin/roles/client/{client_id}/{role_name}` - Mettre à jour un rôle
- `DELETE /admin/roles/client/{client_id}/{role_name}` - Supprimer un rôle
- `POST /admin/users/{user_id}/roles/assign` - Assigner des rôles à un utilisateur
- `POST /admin/users/{user_id}/roles/remove` - Retirer des rôles d'un utilisateur

### Gestion des Realms

- `POST /admin/realms` - Créer un realm
- `GET /admin/realms` - Lister tous les realms
- `GET /admin/realms/{realm_name}` - Récupérer un realm
- `PUT /admin/realms/{realm_name}` - Mettre à jour un realm

### Fournisseurs d'Identité

- `POST /admin/realms/{realm_name}/identity-providers` - Créer un fournisseur d'identité
- `GET /admin/realms/{realm_name}/identity-providers` - Lister les fournisseurs
- `DELETE /admin/realms/{realm_name}/identity-providers/{alias}` - Supprimer un fournisseur

## Authentification OAuth2/OpenID Connect

### Flux d'authentification

1. **Configuration du Client Keycloak**

   - Type : `public` ou `confidential`
   - Flow : Authorization Code Flow ou Client Credentials
   - Redirect URI : `http://localhost:3000/callback`
2. **Obtenir un Token**

```bash
TOKEN=$(curl -s -X POST \
  http://localhost:8080/realms/myrealm/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=<CLIENT_ID>" \
  -d "client_secret=<CLIENT_SECRET>" \
  -d "grant_type=password" \
  -d "username=test" \
  -d "password=test" | jq -r .access_token)

echo $TOKEN

```

3. Utiliser le Token
```bash
curl -i -X GET http://localhost:8000/keycloak-fastapi \
H "Authorization: Bearer ${TOKEN}"
```
### Schéma de sécurité (Optionel)

L'application utilise **OAuth2 avec Password Bearer** :

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

## Modèles de données

### Utilisateur

```python
{
  "username": "john.doe",
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "enabled": true,
  "emailVerified": true
}
```

### Rôle Client

```python
{
  "name": "admin",
  "description": "Administrateur",
  "composite": false
}
```

### Fournisseur d'Identité

```python
{
  "alias": "google",
  "providerId": "google",
  "enabled": true,
  "config": {
    "clientId": "google-client-id",
    "clientSecret": "google-client-secret"
  }
}
```

## Dépannage

### Erreur : "Impossible de se connecter à Keycloak"

- Vérifier que Keycloak est en exécution : `http://localhost:8080`
- Vérifier les variables d'environnement dans `config.py`

### Erreur : "Client non trouvé"

- S'assurer que le `KEYCLOAK_CLIENT_ID` existe dans le realm
- Vérifier les permissions du client administrateur

### Erreur de type "str | None"

- Ajouter des vérifications en début de fonction :

```python
if not user_id or not client_id:
    raise ValueError("Les paramètres ne peuvent pas être None")
```

## Documentation API

Une fois l'application lancée, accéder à :

- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## Licence

MIT

## Contribuer

1. Créer une branche : `git checkout -b feature/ma-feature`
2. Commit : `git commit -m "Ajouter ma feature"`
3. Push : `git push origin feature/ma-feature`
4. Créer une Pull Request
