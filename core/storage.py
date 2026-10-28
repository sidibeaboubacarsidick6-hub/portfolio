"""
Storage Cloudinary custom, compatible Django 6.1+.
Remplace django-cloudinary-storage (incompatible : utilise STATICFILES_STORAGE supprime).
Utilise directement le SDK officiel `cloudinary`.
"""
import os
import cloudinary
import cloudinary.uploader
import cloudinary.utils
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class MediaCloudinaryStorage(Storage):
    """Storage Django qui envoie les fichiers sur Cloudinary et retourne l'URL publique."""

    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True,
        )

    def _save(self, name, content):
        # Upload vers Cloudinary dans un dossier "media/"
        result = cloudinary.uploader.upload(
            content,
            folder="media",
            public_id=os.path.splitext(name)[0],
            resource_type="auto",
            overwrite=False,
        )
        return result["public_id"]

    def url(self, name):
        if not name:
            return ""
        # Cloudinary n'accepte PAS "auto" en URL de livraison (uniquement en upload).
        # On choisit "image" pour les images ET les PDF (Cloudinary traite les PDF
        # comme des images pour permettre les transformations).
        # On garde "raw" en secours pour les autres documents (docx, zip, etc.).
        ext = os.path.splitext(name)[1].lower()
        if ext in (".doc", ".docx", ".zip", ".txt", ".csv"):
            resource_type = "raw"
            url, _ = cloudinary.utils.cloudinary_url(
                name,
                resource_type=resource_type,
                secure=True,
            )
        else:
            resource_type = "image"
            url, _ = cloudinary.utils.cloudinary_url(
                name,
                resource_type=resource_type,
                fetch_format="auto",
                quality="auto",
                secure=True,
            )
        return url

    def exists(self, name):
        return False

    def delete(self, name):
        try:
            cloudinary.uploader.destroy(name, resource_type="auto")
        except Exception:
            pass

    def size(self, name):
        return 0
