from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, SiteContent, Skill, Service
from .forms import ContactForm


def home(request):
    projects = Project.objects.filter(is_featured=True)

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Merci, votre message a bien ete envoye.")
            return redirect("/#contact")
    else:
        form = ContactForm()

    content = SiteContent.load()

    # Decoupe du hero pour colorer le mot-cle
    title = content.hero_title
    hl = content.hero_highlight
    if hl and hl in title:
        idx = title.index(hl)
        hero_before = title[:idx]
        hero_after = title[idx + len(hl):]
    else:
        hero_before = title
        hero_after = ""

    # Tags techniques
    tech_tags = [t.strip() for t in content.hero_tech_tags.split(",") if t.strip()]

    # Competences groupees
    skills = list(Skill.objects.all())
    skills_backend = [s for s in skills if s.category == "backend"]
    skills_frontend = [s for s in skills if s.category == "frontend"]
    skills_deploy = [s for s in skills if s.category == "deploy"]

    services = list(Service.objects.all())

    return render(request, "core/home.html", {
        "projects": projects,
        "form": form,
        "content": content,
        "hero_before": hero_before,
        "hero_after": hero_after,
        "tech_tags": tech_tags,
        "skills_backend": skills_backend,
        "skills_frontend": skills_frontend,
        "skills_deploy": skills_deploy,
        "services": services,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "core/project_detail.html", {"project": project})
