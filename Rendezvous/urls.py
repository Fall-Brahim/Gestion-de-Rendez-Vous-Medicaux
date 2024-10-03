from django.urls import path
from .views import create_rendezvous,MesRendevous,MaRendezVous,confirmer_rendezvous,dashboard,reject_rendezvous,Tableau_de_Bord,MesPatient



urlpatterns = [
    path('doctor/<int:programme_id>/createrdv/',create_rendezvous,name="createrdv"),
    path('patient',MesPatient,name='patient'),
    path('mesrdv/',MesRendevous,name='mesrdv'),
    path('myrdv/',MaRendezVous,name='myrdv'),
    path('confirmer_rendezvous/<int:rendezvous_id>/', confirmer_rendezvous, name='confirmer_rendezvous'),
    path('reject_rendezvous/<int:rendezvous_id>/', reject_rendezvous, name='reject_rendezvous'),
    path('dashboard/',dashboard,name='dashboard'),
    path('medecin/<int:medecin_id>/tableau_de_bord/', Tableau_de_Bord, name='tableau_de_bord'),
]