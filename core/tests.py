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


from django.core import mail


@override_settings(STORAGES=TEST_STORAGES)
class ContactTests(TestCase):
    def envoyer(self, **extra):
        data = {"name": "Awa", "email": "awa@example.com", "message": "Bonjour"}
        data.update(extra)
        return self.client.post(reverse("core:home"), data)

    def test_un_message_declenche_un_email(self):
        self.envoyer()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ["awa@example.com"])

    def test_le_champ_piege_ignore_le_message(self):
        r = self.envoyer(website="http://spam.example")
        self.assertRedirects(r, "/#contact", fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_retour_ligne_dans_le_nom_ne_casse_rien(self):
        r = self.envoyer(name="Awa\nBcc: x@example.com")
        self.assertEqual(r.status_code, 302)
        self.assertNotIn("\n", mail.outbox[0].subject)
