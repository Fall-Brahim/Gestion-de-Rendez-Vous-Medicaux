from django.urls import path
from .views import programme,EmploiDuTemps

urlpatterns =[
    path('programme',programme,name="programme"),
    path('emploi/',EmploiDuTemps,name='emploi')
]