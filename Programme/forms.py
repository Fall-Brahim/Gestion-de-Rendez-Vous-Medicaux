from django import forms
from .models import Programme

class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ['jour', 'mois', 'date', 'debut_heure', 'fin_heure']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'debut_heure': forms.TimeInput(attrs={'type': 'time'}),
            'fin_heure': forms.TimeInput(attrs={'type': 'time'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        debut_heure = cleaned_data.get("debut_heure")
        fin_heure = cleaned_data.get("fin_heure")
        
        if debut_heure and fin_heure and debut_heure >= fin_heure:
            raise ValidationError('L\'heure de début doit être avant l\'heure de fin')
        
        return cleaned_data