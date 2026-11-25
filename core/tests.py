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


from .storage import MediaCloudinaryStorage


class StorageTests(TestCase):
    def test_noms_uniques_et_extension_conservee(self):
        s = MediaCloudinaryStorage()
        a = s.get_available_name("site/photo.jpg")
        b = s.get_available_name("site/photo.jpg")
        self.assertNotEqual(a, b)
        self.assertTrue(a.startswith("site/photo-") and a.endswith(".jpg"))


from django.contrib.auth import get_user_model


@override_settings(STORAGES=TEST_STORAGES)
class AdminDashboardTests(TestCase):
    def test_tableau_de_bord(self):
        admin_user = get_user_model().objects.create_superuser("admin", "a@example.com", "mdp-de-test-12345")
        self.client.force_login(admin_user)
        ContactMessage.objects.create(name="Awa", email="awa@example.com", message="Bonjour")
        r = self.client.get(reverse("admin:index"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Messages non lus")
        self.assertEqual(r.context["dashboard"]["unread"], 1)


@override_settings(STORAGES=TEST_STORAGES)
class PublicationTests(TestCase):
    def setUp(self):
        self.brouillon = Project.objects.create(
            title="Brouillon secret", summary="r", description="d",
            stack="Django", role="Dev", is_featured=False,
        )
        self.url = reverse("core:project_detail", args=[self.brouillon.slug])

    def test_brouillon_invisible_aux_visiteurs(self):
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertNotContains(self.client.get(reverse("core:home")), "Brouillon secret")

    def test_brouillon_visible_pour_le_staff(self):
        staff = get_user_model().objects.create_user(
            "staff", "s@example.com", "mdp-de-test-12345", is_staff=True,
        )
        self.client.force_login(staff)
        self.assertEqual(self.client.get(self.url).status_code, 200)
