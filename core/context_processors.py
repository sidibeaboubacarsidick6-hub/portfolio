import os
from django.conf import settings


def static_version(request):
    """Retourne un numero de version base sur la mtime de output.css
    pour eviter que le navigateur serve une version en cache apres rebuild."""
    try:
        path = os.path.join(settings.BASE_DIR, "static", "css", "output.css")
        mtime = os.path.getmtime(path)
        return {"STATIC_VERSION": str(int(mtime))}
    except OSError:
        return {"STATIC_VERSION": "0"}


from .models import SiteContent

def get_site_content(request):
    """Charge SiteContent une seule fois par requete."""
    if not hasattr(request, "_site_content"):
        request._site_content = SiteContent.load()
    return request._site_content


def site_content(request):
    return {'content': get_site_content(request)}
