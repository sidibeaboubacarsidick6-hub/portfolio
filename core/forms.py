from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Champ piège anti-spam : invisible pour les humains, rempli par les robots.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "field", "placeholder": "Votre nom", "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "field", "placeholder": "votre@email.com", "autocomplete": "email",
            }),
            "message": forms.Textarea(attrs={
                "class": "field", "placeholder": "Votre message...", "rows": 5,
            }),
        }
