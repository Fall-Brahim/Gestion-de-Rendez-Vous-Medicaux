from django.urls import path
from .views import home,RegisterMedecin,RegisterPatient,liste_patiens,all_users,activate,doctors,doctor_detail,Login,LogOut,profile_patient,mark_as_read,Editer_Medecin,Editer_Patient


urlpatterns = [
    path('',home,name="home"),
    path('register/',RegisterMedecin,name='register'),
    path('signUp/',RegisterPatient,name="signUp"),
    path('editeMedecin',Editer_Medecin,name="editeMedecin"),
    path('editePatient',Editer_Patient,name="editePatient"),
    path('doctors/',doctors,name="doctors"),
    path('doctor/<int:id>/',doctor_detail, name='doctor_detail'),
    path('patientProf/<int:Id>/',profile_patient,name='patientProf'),
    path('notifications/read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('all_users',all_users,name='all_users'),
    path('activate/<int:medecin_id>',activate,name='activate'),
    path('liste_patients/',liste_patiens,name='liste_patients'),
    path('logine/',Login,name='logine'),
    path('logout/',LogOut,name='logout'),        
]