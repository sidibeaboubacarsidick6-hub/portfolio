from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "stack", "is_featured", "order", "updated_at")
    list_editable = ("is_featured", "order")
    search_fields = ("title", "stack", "summary")
    prepopulated_fields = {"slug": ("title",)}


from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")


from .models import SiteContent, Skill, Service


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero", {
            "fields": ("hero_badge", "hero_title", "hero_highlight", "hero_subtitle", "hero_tech_tags"),
        }),
        ("À propos", {
            "fields": ("about_p1", "about_p2", "about_p3"),
        }),
        ("Contact", {
            "fields": ("contact_intro", "contact_email"),
        }),
        ("Liens professionnels", {
            "fields": ("github_url", "linkedin_url", "cv_file"),
        }),
        ("Footer", {
            "fields": ("footer_tagline", "site_background"),
        }),
    )

    def has_add_permission(self, request):
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_editable = ("category", "order")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("icon", "order")
    search_fields = ("title", "description")
