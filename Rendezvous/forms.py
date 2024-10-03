from django import forms
from .models import RendezVous

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['motif', 'notes']  # Exclude 'medecin' and 'status' as these will be set in the view
