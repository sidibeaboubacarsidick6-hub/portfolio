# Guide de maintenance — Portfolio

Ce document décrit les tâches courantes : modifier le contenu, travailler en local, publier, sauvegarder et dépanner.

## Accès

| Service | URL |
| --- | --- |
| Site en production | https://portfolio-sidick.onrender.com |
| Administration | https://portfolio-sidick.onrender.com/admin/ |
| Tableau de bord Render | https://dashboard.render.com |
| Console Cloudinary | https://console.cloudinary.com |
| Dépôt GitHub | https://github.com/sidibeaboubacarsidick6-hub/portfolio |

## Modifier le contenu (sans toucher au code)

Connexion à `/admin/` avec le compte superutilisateur. La page d'accueil de l'admin est un tableau de bord : messages non lus, projets publiés, raccourcis et derniers messages.

- **Contenu du site** : hero (avec photo), à propos, contact, liens, CV, pied de page, image de fond.
- **Projets** : cartes et études de cas. La case **Publié** décide de la visibilité : décochée, le projet disparaît de l'accueil et sa page renvoie une 404 aux visiteurs. Connecté à l'admin, tu le vois quand même (utile pour relire avant de publier).
- **Compétences** : par catégorie (backend, frontend, déploiement et outils).
- **Services** : les cartes de services.
- **Messages de contact** : à consulter et marquer comme lus.

### Images

Toutes les images envoyées via l'admin sont stockées sur Cloudinary, avec un nom unique ajouté automatiquement (un fichier du même nom n'écrase plus l'ancien).

- **Image de couverture d'un projet** : Admin > Projets > champ « Cover image ». JPG ou PNG, 1200x675 px (16:9), moins de 500 Ko.
- **Photo du hero** : Admin > Contenu du site > « Hero photo ». Carrée, 1000x1000 px conseillé. Si le champ est vide, le hero s'affiche en pleine largeur.
- **Image de fond du site** : Admin > Contenu du site > section Footer.

### CV

Admin > Contenu du site > « Cv file » (PDF, DOC ou DOCX, 5 Mo maximum). Le bouton « Télécharger mon CV » apparaît automatiquement.

## Messages de contact et alertes e-mail

Chaque message du formulaire est enregistré dans l'admin **et** envoyé par e-mail à l'adresse « contact_email » (Admin > Contenu du site). Le champ « Répondre à » est celui de l'expéditeur : tu peux répondre directement depuis ta boîte mail. Un champ piège invisible bloque les robots.

L'envoi utilise Gmail avec un **mot de passe d'application** (validation en deux étapes obligatoire sur le compte Google, puis « Mots de passe d'application » dans la page Sécurité). Ne jamais mettre ce mot de passe dans Git.

Si les alertes n'arrivent plus : Render > Logs, chercher « Echec de l'envoi de l'alerte e-mail de contact ». Les messages restent enregistrés dans l'admin même si l'e-mail échoue.

## Travailler en local

```bash
source .venv/bin/activate
./dev.sh                  # Tailwind (watch) + serveur sur http://localhost:8000
python manage.py test     # tests automatiques
npm run build             # CSS minifié (sans le mode watch)
```

- Migrations après un changement de modèle : `python manage.py makemigrations` puis `python manage.py migrate`.
- Sans `EMAIL_BACKEND` dans le `.env`, les e-mails s'affichent dans le terminal au lieu d'être envoyés.
- **Attention :** les images envoyées depuis l'admin local partent sur le même compte Cloudinary que la production.

Répétition en mode production (avant un déploiement important) :

```bash
npm run build
DEBUG=False python manage.py collectstatic --noinput
DEBUG=False ALLOWED_HOSTS=localhost,127.0.0.1 gunicorn config.wsgi:application --bind 127.0.0.1:8001
```

Sur `http://127.0.0.1:8001`, le formulaire et la connexion admin peuvent échouer : les cookies sont réservés au HTTPS en production.

## Publier une modification

```bash
git switch -c ma-modification
# ... modifications, puis :
python manage.py test
git add <fichiers>
git commit -m "description du changement"
git push -u origin ma-modification
git switch main
git merge --no-ff ma-modification
git push origin main
```

Render redéploie à chaque push sur `main` en exécutant `build.sh` : installation des dépendances Python et Node, build Tailwind, collecte des statiques, migrations, chargement des données initiales (seulement si la base est vide), création du superutilisateur (si absent).

## Variables d'environnement

| Variable | Rôle |
| --- | --- |
| `DEBUG` | `True` en local, `False` en production |
| `SECRET_KEY` | clé secrète (générée par Render en production) |
| `ALLOWED_HOSTS` | hôtes autorisés, séparés par des virgules |
| `DATABASE_URL` | base PostgreSQL (fournie par Render ; absente en local = SQLite) |
| `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` | stockage des images |
| `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT` | serveur d'e-mail (Gmail : `smtp.gmail.com`, 587) |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` | identifiants et expéditeur |
| `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` | compte admin créé au build |
| `SECURE_HSTS_SECONDS` | durée HSTS en secondes (3600 par défaut ; à allonger après vérification) |
| `SECURE_SSL_REDIRECT` | `True` pour forcer la redirection HTTPS côté Django (Render la fait déjà) |

Les variables marquées `sync: false` dans `render.yaml` se saisissent à la main dans Render > Environment, jamais dans Git.

## Sauvegarder la base de données

La base gratuite de Render **expire 30 jours après sa création**. Exporte régulièrement le contenu (textes, projets, messages) :

```bash
python manage.py dumpdata --indent 2 > backup_$(date +%Y%m%d).json
```

Avec `DATABASE_URL` pointant vers la production, c'est la base en ligne qui est exportée ; sans, c'est ta base locale. Pour restaurer : `python manage.py loaddata backup_AAAAMMJJ.json`. Les fichiers `backup_*.json` contiennent des messages de visiteurs : ne jamais les ajouter à Git. Les images sont sur Cloudinary et ne dépendent pas de cette base.

## Revenir en arrière après un déploiement raté

```bash
git switch main
git log --oneline --merges -3        # repérer le commit de fusion
git revert -m 1 <hash-du-merge>
git push origin main
```

Render redéploie la version précédente. Le repère `pre-redesign` (s'il existe) marque l'état de `main` avant la refonte : `git log pre-redesign` pour le consulter.

## Dépannage

**Erreur 500** : Render > service portfolio-sidick > Logs, chercher `Traceback` ou `Error`. Causes fréquentes : variable d'environnement manquante ou mal orthographiée, migration non appliquée, base expirée, clés Cloudinary invalides.

**Service suspendu** : le plan gratuit de Render offre 750 heures par mois, partagées entre tous les services gratuits du compte. En cas de dépassement, le service est suspendu jusqu'au début du mois suivant, ou jusqu'au passage à une instance payante. Un service gratuit s'endort après 15 minutes sans visite et ne consomme alors pas d'heures : vérifier qu'aucun outil ne le réveille en permanence.

**Renouveler les clés Cloudinary** (si elles sont compromises) : Cloudinary > Settings > API Keys > Regenerate, mettre à jour le `.env` local et Render > Environment (3 variables), puis attendre le redéploiement.

## Support

- Render : https://render.com/docs
- Django : https://docs.djangoproject.com
- Cloudinary : https://cloudinary.com/documentation

Dernière mise à jour : novembre 2026
