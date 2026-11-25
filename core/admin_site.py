from django.contrib.admin import AdminSite


class PortfolioAdminSite(AdminSite):
    site_header = "Portfolio — administration"
    site_title = "Portfolio"
    index_title = "Tableau de bord"

    def index(self, request, extra_context=None):
        from .models import ContactMessage, Project, Service, Skill

        extra = {
            "dashboard": {
                "unread": ContactMessage.objects.filter(is_read=False).count(),
                "messages": ContactMessage.objects.count(),
                "projects_published": Project.objects.filter(is_featured=True).count(),
                "projects": Project.objects.count(),
                "skills": Skill.objects.count(),
                "services": Service.objects.count(),
                "latest": list(ContactMessage.objects.all()[:5]),
            }
        }
        extra.update(extra_context or {})
        return super().index(request, extra)
