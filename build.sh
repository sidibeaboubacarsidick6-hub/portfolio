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

echo "==> Chargement des donnees initiales"
python manage.py loaddata fixtures/core_data.json || echo "Donnees deja presentes, skip."

echo "==> Creation du superutilisateur (si absent)"
python manage.py createsuperuser --noinput || echo "Superutilisateur deja existant, skip."

echo "==> Build termine avec succes"
