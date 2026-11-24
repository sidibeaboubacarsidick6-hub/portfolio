from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage, Project

TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}


@override_settings(STORAGES=TEST_STORAGES)
class SmokeTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Projet test", summary="Résumé", description="Description",
            stack="Django", role="Développeur",
        )

    def test_accueil(self):
        r = self.client.get(reverse("core:home"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Projet test")

    def test_detail_projet(self):
        r = self.client.get(reverse("core:project_detail", args=[self.project.slug]))
        self.assertEqual(r.status_code, 200)

    def test_projet_inconnu_404(self):
        self.assertEqual(self.client.get("/projets/inexistant/").status_code, 404)

    def test_formulaire_contact(self):
        r = self.client.post(reverse("core:home"), {
            "name": "Awa", "email": "awa@example.com", "message": "Bonjour",
        })
        self.assertRedirects(r, "/#contact", fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)
