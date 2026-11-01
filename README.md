# NEVARA Classroom V2

Plateforme unifiée d’accompagnement académique : catalogue sécurisé, wallet/ledger, arbre binaire d’engagement, parrainage, forum.

**Repo :** https://github.com/ghenysis/nevara-classroom  
**Version :** 2.0.0

## Stack

- **Backend :** Django + DRF + Celery + Redis + SQLite/Postgres
- **Frontend :** React + Vite + TypeScript + Tailwind

## Démarrage local (tests)

### Prérequis
- Python 3.11+
- Node 20+
- Redis (pour Celery beat — optionnel en dev)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # ajuster SECRET_KEY, FRONTEND_BASE_URL, REDIS_URL
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

API : `http://localhost:8000/api/v1/`  
Health : `http://localhost:8000/api/v1/health/`

### Frontend

```bash
cd frontend
cp .env.example .env       # VITE_API_BASE_URL=http://localhost:8000/api/v1
npm install
npm run dev
```

App : `http://localhost:5173`

### Celery (cron réseau 30h + abonnements)

```bash
celery -A core worker -l info
celery -A core beat -l info
```

## Fonctionnalités V2

- Wallet : dépôts, retraits, topup abonnement avec vérification de solde
- Arbre binaire : spillover + niveau d’engagement basé sur parrainage direct (F1/équipe)
- Vue personnelle arbre : vous en racine + descendants uniquement
- Commissions cycle 3,7 % bornées par le niveau de chaque ascendant
- Thèmes clair / sombre / système
- Auth JWT + refresh, cache wallet, endpoint health

## Structure

```
backend/     Django apps: users, wallet, tree, referral, catalog, forum
frontend/    React (src/components, api, stores, context)
```
