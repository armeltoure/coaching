from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'phone_number', 'email', 'ticket_quantity', 'message']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('+225'):
            phone_number = '+225' + phone_number.lstrip('0')
        return phone_number

class CommandeForm(forms.Form):
    nom = forms.CharField(label="Nom et Prénoms", max_length=100)
    quantite = forms.IntegerField(label="Quantité", min_value=1)
    numero = forms.CharField(label="Numéro de téléphone", max_length=20)
    lieu_livraison = forms.CharField(label="Lieu de livraison", max_length=200)
