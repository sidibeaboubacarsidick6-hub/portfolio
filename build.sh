#!/usr/bin/env bash
# Script de build execute par Render a chaque deploiement.
set -o errexit

echo "==> Installation des dependances Python"
pip install -r requirements.txt

echo "==> Installation des dependances Node (Tailwind)"
npm ci

echo "==> Build du CSS Tailwind (mode production, minifie)"
npm run build

echo "==> Collecte des fichiers statiques"
python manage.py collectstatic --noinput

echo "==> Application des migrations"
python manage.py migrate

echo "==> Chargement des donnees initiales (seulement si base vide)"
python manage.py shell -c "
from core.models import Project
if Project.objects.exists():
    print('Donnees presentes en base, skip loaddata.')
else:
    from django.core.management import call_command
    call_command('loaddata', 'fixtures/core_data.json')
    print('Donnees initiales chargees.')
"

echo "==> Creation du superutilisateur (si absent)"
python manage.py createsuperuser --noinput || echo "Superutilisateur deja existant, skip."

echo "==> Build termine avec succes"
