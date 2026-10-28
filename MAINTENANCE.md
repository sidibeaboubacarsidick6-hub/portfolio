# Guide de maintenance — Portfolio

Ce document explique comment effectuer les tâches courantes sur le portfolio en production.

Accès
Service	URL
Site en production	https://portfolio-sidick.onrender.com
Admin Django	https://portfolio-sidick.onrender.com/admin/
Dashboard Render	https://dashboard.render.com
Console Cloudinary	https://console.cloudinary.com
Modifier le contenu du site
Tout le contenu est modifiable depuis l'admin Django. Aucun code à toucher.

Se connecter à /admin/ avec le compte superutilisateur

Contenu du site : hero, à propos, contact, liens, CV

Projets : ajouter ou éditer les cartes de projets

Compétences : gérer les skills par catégorie (backend/frontend/deploy)

Services : gérer les 4 cartes de services

Messages de contact : consulter et marquer comme lus les messages reçus

Ajouter une image à un projet
Admin > Projets > sélectionner le projet

Champ Image de couverture > Choisir un fichier

Enregistrer : l'image est automatiquement uploadée sur Cloudinary

Format recommandé : JPG ou PNG, 1200x675 px (ratio 16:9), moins de 500 Ko.

Mettre à jour le CV
Admin > Contenu du site

Section Liens professionnels > champ Cv file

Uploader le nouveau PDF (max 5 Mo, formats acceptés : PDF, DOC, DOCX)

Enregistrer : le bouton Télécharger mon CV apparaît automatiquement sur le site

Sauvegarder la base de données
Option A - Depuis Render (recommandée) :

Dashboard Render > base portfolio-db > onglet Backups

Render fait des sauvegardes automatiques quotidiennes (7 jours sur le plan gratuit)

Cliquer sur Download pour récupérer un backup

Option B - Export manuel via Django (en local, avec DATABASE_URL pointant vers la prod) :

bash
python manage.py dumpdata > backup_$(date +%Y%m%d).json
Mettre à jour le code
bash
# 1. Faire les modifications en local
# 2. Tester en local (python manage.py runserver)
# 3. Committer et pousser
git add .
git commit -m "description du changement"
git push origin main
Render détecte automatiquement le push et redéploie en 2-3 min.

Si le site est en erreur 500
Aller sur Render > service portfolio-sidick > Logs

Chercher les lignes Traceback ou Error

Causes fréquentes :

Variable d'environnement manquante ou mal orthographiée

Migration non appliquée (relancer python manage.py migrate)

Base Postgres en limite de quota

Renouveler les clés Cloudinary
Si les clés ont été compromises :

Cloudinary > Settings > API Keys > Regenerate

Mettre à jour .env local (2 lignes)

Mettre à jour Render > Environment (2 variables)

Attendre le redéploiement automatique (2 min)

Support
Documentation Render : https://render.com/docs

Documentation Django : https://docs.djangoproject.com

Documentation Cloudinary : https://cloudinary.com/documentation

Dernière mise à jour : Octobre 2026
