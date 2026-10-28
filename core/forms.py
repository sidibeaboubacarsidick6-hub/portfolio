from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-sm text-ink placeholder-black/40 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 transition",
                "placeholder": "Votre nom",
                "required": True,
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-sm text-ink placeholder-black/40 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 transition",
                "placeholder": "votre@email.com",
                "required": True,
            }),
            "message": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-black/10 bg-white px-4 py-3 text-sm text-ink placeholder-black/40 focus:border-accent focus:outline-none focus:ring-2 focus:ring-accent/20 transition",
                "placeholder": "Votre message...",
                "rows": 5,
                "required": True,
            }),
        }
