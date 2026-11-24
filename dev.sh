#!/usr/bin/env bash
# Lance Tailwind (watch) et Django ensemble. Arrêt avec Ctrl+C.
set -e
npm run watch &
TW_PID=$!
trap 'kill $TW_PID 2>/dev/null' EXIT
python manage.py runserver
