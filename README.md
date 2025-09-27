# Ticket Management API — FastAPI

Mini projet d’entretien — **API de gestion de tickets** réalisée avec **FastAPI**, **SQLAlchemy**, et **Pydantic**.  
Base de données : **SQLite en mémoire**.

---

## Fonctionnalités

- `POST /tickets/` → créer un ticket  
- `GET /tickets/` → lister tous les tickets  
- `GET /tickets/{ticket_id}` → récupérer un ticket par ID  
- `PUT /tickets/{ticket_id}` → mettre à jour un ticket  
- `PATCH /tickets/{ticket_id}/close` → fermer un ticket
- `GET /health` → endpoint santé  

---

## Installation locale

### 1) Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 2) Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3) Lancer l’application
```bash
uvicorn app.main:app --reload --port 8010
```
🥲 désolé le port 8000 est occupé chez moi 😁

Accéder à la doc : [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs)

---

## Tests

### Lancer les tests
```bash
pytest
```

### Lancer les tests avec couverture
```bash
pytest --cov=app --cov-report=term-missing
```

### Vérifier le lint avec Ruff
```bash
ruff check .
```

### Corriger automatiquement le lint
```bash
ruff check . --fix
```

---

## Utilisation avec Docker

### 1) Construire l’image
```bash
docker build -t fastapi-tickets .
```

### 2) Lancer le conteneur
```bash
docker run --rm -p 8010:8010 fastapi-tickets
```

L’API est dispo sur [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs).

---

## Utilisation avec Makefile

Un `Makefile` est fourni pour simplifier les commandes :

```bash
make run       # lancer l'API
make test      # lancer les tests
make cov       # couverture
make lint      # linting
make fmt       # corriger le lint
make docker-build
make docker-run
```

---

## Structure du projet

```
app/
├── core/           # config (db, logging)
├── models/         # modèles SQLAlchemy
├── repositories/   # accès DB (CRUD)
├── routers/        # endpoints
├── schemas/        # schémas Pydantic
└── main.py         # point d'entrée
tests/              # tests Pytest
requirements.txt    # dépendances
Dockerfile          # build image Docker
Makefile            # (optionnel) raccourcis
```

---

## Exemple d'utilisation (via cURL)

Créer un ticket :
```bash
curl -X POST http://127.0.0.1:8010/tickets/     -H "Content-Type: application/json"     -d '{"title": "Bug critique", "description": "Impossible de sauvegarder"}'
```

Réponse attendue :
```json
{
  "id": 1,
  "title": "Bug critique",
  "description": "Impossible de sauvegarder",
  "status": "open",
  "created_at": "2025-09-28T12:34:56.789Z"
}
```

Fermer le ticket :
```bash
curl -X PATCH http://127.0.0.1:8010/tickets/1/close
```

---

## Auteur

Projet d’entretien — **Houssem Eddine Selmi**
