from django import forms
from .models import Utilisateur, Medecin, Patient
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Medecin
        fields = ['nom', 'prenom', 'email', 'profil', 'genre','specialite','informations_contact','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Les champs de mot de passe ne correspondent pas."
            )
            

class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'email', 'profil', 'genre','numero_telephone','adresse','date_naissance','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Les champs de mot de passe ne correspondent pas."
            )
            
from django.contrib.auth import get_user_model      

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)
    


# Editer medecin et Patient



class EditMedecinForm(forms.ModelForm):
    class Meta:
        model = Medecin
        fields =  ['nom', 'prenom', 'email', 'profil', 'genre','specialite','informations_contact']
        
        
class EditePatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'email', 'profil', 'genre','numero_telephone','adresse','date_naissance']