from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(max_length=200, help_text="Resume court affiche sur la carte")
    description = models.TextField(help_text="Description detaillee (etude de cas)")
    stack = models.CharField(max_length=200, help_text="Ex: Django, PostgreSQL, Bootstrap")
    role = models.CharField(max_length=160, help_text="Ex: Developpeur unique, conception a la mise en production")
    demo_url = models.URLField(blank=True, help_text="Lien vers la demo en ligne")
    github_url = models.URLField(blank=True, help_text="Lien vers le depot (laisser vide si prive)")
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage (croissant)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.created_at:%d/%m/%Y}"


class SiteContent(models.Model):
    """Singleton : une seule ligne en base pour le contenu global du site."""

    # Hero
    hero_badge = models.CharField(max_length=120, default="Développeur full-stack junior")
    hero_title = models.CharField(
        max_length=200,
        default="Je transforme les idées en applications web concrètes.",
    )
    hero_highlight = models.CharField(
        max_length=80,
        default="applications web",
        help_text="Mot ou groupe de mots à colorer en accent dans le titre",
    )
    hero_subtitle = models.TextField(
        default="Du développement backend à la mise en production, je conçois des solutions numériques fonctionnelles, pensées pour répondre aux besoins réels des entreprises et de leurs utilisateurs."
    )
    hero_tech_tags = models.CharField(
        max_length=255,
        default="Python & Django,API REST,Bases de données,Déploiement web",
        help_text="Tags séparés par des virgules",
    )

    # À propos
    about_p1 = models.TextField(default="Je suis développeur informatique, orienté vers le développement web, les applications métier et les solutions numériques.")
    about_p2 = models.TextField(default="Mon approche ne s'arrête pas au code. Je m'intéresse également à l'intégration des interfaces, à la connexion des API, à la préparation des environnements techniques et au déploiement des applications en production.")
    about_p3 = models.TextField(default="À travers mes projets, je cherche à renforcer mes compétences, à résoudre des problèmes concrets et à construire des solutions fiables, maintenables et adaptées aux besoins de leurs utilisateurs.")

    # Contact
    contact_intro = models.TextField(
        default="Une idée à concrétiser, un besoin technique ou une opportunité professionnelle ? Décrivez-moi votre projet et voyons comment avancer ensemble."
    )
    contact_email = models.EmailField(default="sidibeaboubacarsidick6@gmail.com")

    # Liens pro
    github_url = models.URLField(default="https://github.com/sidibeaboubacarsidick6-hub", blank=True)
    linkedin_url = models.URLField(blank=True, default="#")

    # CV
    cv_file = models.FileField(
        upload_to="cv/",
        blank=True,
        null=True,
        help_text="PDF recommande (max 5 Mo). Apparait comme bouton sur le site.",
    )

    # Footer
    footer_tagline = models.CharField(max_length=160, default="Abidjan, Côte d'Ivoire")

    class Meta:
        verbose_name = "Contenu du site"
        verbose_name_plural = "Contenu du site"

    def __str__(self):
        return "Contenu du site"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.cv_file and hasattr(self.cv_file, "size"):
            if self.cv_file.size > 5 * 1024 * 1024:
                from django.core.exceptions import ValidationError
                raise ValidationError({"cv_file": "Le CV ne doit pas depasser 5 Mo."})
            name = (self.cv_file.name or "").lower()
            if not name.endswith((".pdf", ".doc", ".docx")):
                from django.core.exceptions import ValidationError
                raise ValidationError({"cv_file": "Formats acceptes : PDF, DOC, DOCX."})

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Skill(models.Model):
    CATEGORY_BACKEND = "backend"
    CATEGORY_FRONTEND = "frontend"
    CATEGORY_DEPLOY = "deploy"
    CATEGORY_CHOICES = [
        (CATEGORY_BACKEND, "Backend"),
        (CATEGORY_FRONTEND, "Frontend"),
        (CATEGORY_DEPLOY, "Déploiement & outils"),
    ]

    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

    def __str__(self):
        return f"{self.get_category_display()} — {self.name}"


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=8, default="↗", help_text="Petit caractère affiché en icône (ex: </>, { }, ↗, ▤)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title
