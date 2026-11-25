# Portfolio — Sidibe Aboubacar Sidick

Portfolio professionnel de développeur full-stack junior, conçu et développé de bout en bout avec Django.

**En production :** https://portfolio-sidick.onrender.com

## Fonctionnalités

- Design responsive (Tailwind CSS) : système de composants, contrastes conformes AA, animations au scroll respectant `prefers-reduced-motion`
- Administration complète : textes, photo du hero, projets, compétences et services modifiables sans toucher au code
- Tableau de bord d'administration : messages non lus, projets publiés, raccourcis
- Projets avec statut **Publié / brouillon** : un brouillon est invisible des visiteurs, visible pour le staff
- Formulaire de contact avec protection anti-spam, stockage en base et alerte e-mail
- Images optimisées via Cloudinary (CDN, formats modernes automatiques)
- SEO : métadonnées Open Graph par page, JSON-LD, favicon
- Pages d'erreur personnalisées (404, 500)
- Production durcie : cookies sécurisés, HSTS progressif, en-tête de proxy HTTPS

## Stack technique

| Couche | Technologie |
| :--- | :--- |
| Backend | Python 3.12, Django 6.1 |
| Base de données | PostgreSQL (production), SQLite (développement) |
| Frontend | Tailwind CSS 3.4, JavaScript vanilla |
| Images | Cloudinary |
| Déploiement | Render (Gunicorn, Whitenoise) |

## Lancer le projet en local

Prérequis : Python 3.12+, Node.js 20+, Git.

```bash
git clone https://github.com/sidibeaboubacarsidick6-hub/portfolio.git
cd portfolio

python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate

pip install -r requirements.txt
npm install

# Créer le fichier .env (voir ci-dessous)

python manage.py migrate
python manage.py loaddata fixtures/core_data.json
python manage.py createsuperuser

./dev.sh                         # Tailwind (watch) + serveur sur http://localhost:8000
```

Admin : http://localhost:8000/admin/

## Tests

```bash
python manage.py test
```

## Variables d'environnement (`.env`)

```env
DEBUG=True
SECRET_KEY=une-cle-secrete-unique
ALLOWED_HOSTS=localhost,127.0.0.1

# Cloudinary (obligatoire pour envoyer des images)
CLOUDINARY_CLOUD_NAME=votre-cloud-name
CLOUDINARY_API_KEY=votre-api-key
CLOUDINARY_API_SECRET=votre-api-secret

# E-mail (facultatif en local : sans EMAIL_BACKEND, les e-mails s'affichent dans le terminal)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre-adresse
EMAIL_HOST_PASSWORD=mot-de-passe-d-application
DEFAULT_FROM_EMAIL=Portfolio <votre-adresse>
```

La liste complète des variables, y compris celles de production, est dans `MAINTENANCE.md`.

## Déploiement

Déploiement automatique via Render à chaque push sur `main` : `build.sh` installe les dépendances, compile Tailwind, collecte les statiques, applique les migrations et charge les données initiales si la base est vide. La procédure de publication, de sauvegarde et de retour arrière est décrite dans `MAINTENANCE.md`.

## Licence

© Sidibe Aboubacar Sidick — Tous droits réservés.
