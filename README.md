# Portfolio — Sidibe Aboubacar Sidick

Portfolio professionnel de développeur full-stack junior, conçu et développé de bout en bout avec Django.

**En production :** [https://portfolio-sidick.onrender.com](https://portfolio-sidick.onrender.com)

## Fonctionnalités

- Design premium & responsive (Tailwind CSS, animations au scroll, header sticky)
- Interface d'administration complète : tous les textes, projets, compétences et services sont modifiables depuis l'admin (aucun code à toucher)
- Gestion des projets : cartes avec images, études de cas détaillées, liens démo/GitHub
- Formulaire de contact fonctionnel avec stockage en base et notification dans l'admin
- Optimisation des images via Cloudinary (CDN, conversion WebP/AVIF automatique)
- SEO : métadonnées Open Graph par page, JSON-LD, favicon
- Pages d'erreur custom (404, 500)
- Bilingue prêt (structure i18n en place, traduction FR/EN à activer)

## Stack technique

| Couche | Technologie |
| :--- | :--- |
| Backend | Python 3.12, Django 6.1 |
| Base de données | PostgreSQL (production), SQLite (développement) |
| Frontend | Tailwind CSS 3.4, JavaScript vanilla |
| Images | Cloudinary (CDN + optimisation) |
| Déploiement | Render (Gunicorn, Whitenoise) |

## Lancer le projet en local

Prérequis : Python 3.12+, Node.js 20+, Git.

```bash
# 1. Cloner le dépôt
git clone https://github.com/sidibeaboubacarsidick6-hub/portfolio.git
cd portfolio

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
npm install

# 4. Configurer les variables d'environnement
# Créer un fichier .env avec les valeurs décrites ci-dessous

# 5. Appliquer les migrations et charger les données de démo
python manage.py migrate
python manage.py loaddata fixtures/core_data.json

# 6. Créer un superutilisateur
python manage.py createsuperuser

# 7. Builder le CSS
npm run build

# 8. Lancer le serveur
python manage.py runserver
Site sur http://localhost:8000 — Admin sur http://localhost:8000/admin/.

Variables d'environnement (.env)
env
DEBUG=True
SECRET_KEY=une-cle-secrete-unique
ALLOWED_HOSTS=localhost,127.0.0.1

# Cloudinary (obligatoire pour les images)
CLOUDINARY_CLOUD_NAME=votre-cloud-name
CLOUDINARY_API_KEY=votre-api-key
CLOUDINARY_API_SECRET=votre-api-secret
Déploiement
Déploiement automatisé via Render :

Push sur la branche main

Render détecte le changement et lance build.sh

Le script installe les dépendances, build Tailwind, collecte les statiques, migre la base et redémarre Gunicorn

Licence
© Sidibe Aboubacar Sidick — Tous droits réservés.
