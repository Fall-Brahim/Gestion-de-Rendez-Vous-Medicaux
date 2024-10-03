from django.contrib import admin
from Rendezvous.models import RendezVous
from .models import Utilisateur,Medecin,Patient

# Register your models here.
class MedecinAdmin(admin.ModelAdmin):
    list_display = ['prenom','nom','email','specialite']
    search_fields = ['prenom','nom','email','specialite']
    list_per_page = 5
    

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ['prenom','nom','email']
    search_fields = ['prenom','nom','email']
    list_per_page = 5
    
admin.site.register(Medecin,MedecinAdmin)
admin.site.register(Utilisateur,UtilisateurAdmin)
admin.site.register(RendezVous)