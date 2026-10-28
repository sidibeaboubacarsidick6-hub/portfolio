#!/usr/bin/env bash
# Script de build execute par Render a chaque deploiement.
set -o errexit  # stop si une commande echoue

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

echo "==> Build termine avec succes"
