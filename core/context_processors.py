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
