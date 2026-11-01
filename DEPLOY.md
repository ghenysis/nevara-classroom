# Déploiement NEVARA Classroom V2

## 1. Pousser le code complet (une fois)

Depuis le ZIP `nevara-classroom-v2.zip` :

```bash
git clone https://github.com/ghenysis/nevara-classroom.git
cd nevara-classroom
# Extraire le ZIP et copier le contenu de archive nevara-classroom/
unzip -o ../nevara-classroom-v2.zip
cp -a "archive nevara-classroom"/. .
rm -rf "archive nevara-classroom"
git add -A
git commit -m "feat: NEVARA Classroom V2 — code complet"
git push origin main
```

## 2. Backend (Render / Railway / Fly.io)

### Render (recommandé pour tests)

1. New → Web Service → connecter le repo GitHub
2. Root Directory: `backend`
3. Build Command:
   ```
   pip install -r requirements.txt && python manage.py migrate --noinput
   ```
4. Start Command:
   ```
   gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
   ```
5. Variables d'environnement:
   - `SECRET_KEY` = (générer une clé longue)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `.onrender.com`
   - `FRONTEND_BASE_URL` = URL Vercel du front
   - `REDIS_URL` = (Upstash gratuit ou Redis Render)
   - `DATABASE_URL` = (Postgres Render)

### Celery (optionnel pour tests)
Worker + Beat séparés avec la même image, commandes:
- `celery -A core worker -l info`
- `celery -A core beat -l info`

## 3. Frontend (Vercel)

1. https://vercel.com/new → Import `ghenysis/nevara-classroom`
2. **Root Directory**: `frontend`
3. Framework: Vite
4. Env:
   - `VITE_API_BASE_URL` = `https://VOTRE-BACKEND.onrender.com/api/v1`
5. Deploy

## 4. Checklist tests

- [ ] `GET /api/v1/health/` → ok
- [ ] Register / Login
- [ ] Wallet summary (avec token)
- [ ] Topup abonnement (solde suffisant)
- [ ] Page arbre (descendants only)
- [ ] Thème clair / sombre / système

## 5. CORS

Dans `backend/core/settings/base.py`, autoriser l'origine Vercel:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://votre-app.vercel.app",
]
```
