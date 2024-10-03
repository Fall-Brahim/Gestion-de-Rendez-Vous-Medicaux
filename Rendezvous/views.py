from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Users.models import Medecin,Notifications,Patient
from .models import RendezVous,send_notification_on_create_or_update
from .forms import RendezVousForm
from Programme.models import Programme



@login_required
def create_rendezvous(request, programme_id):
    programme = get_object_or_404(Programme, id=programme_id)
    medecin = programme.medecin
    
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            rendezvous = form.save(commit=False)
            rendezvous.programme = programme
            rendezvous.medecin = medecin
            rendezvous.patient = request.user.patient
            rendezvous.status = 'EN_ATTENTE'
            rendezvous.save()
            
            Notifications.objects.create(
                users=medecin,
                message=f"Vous avez un nouveau rendez-vous avec {rendezvous.patient.prenom} {rendezvous.patient.nom}."
            )
            return redirect('doctor_detail', id=medecin.id)
    else:
        form = RendezVousForm()

    context = {
        'form': form,
        'medecin': medecin,
        'programme':programme
    }
    return render(request, 'rendezvous/RDVForm.html', context)


@login_required
def MesRendevous(request):
    medecin = RendezVous.objects.filter(medecin=request.user.medecin,status ='EN_ATTENTE')
    context ={
        'medecin':medecin,
    }
    return render(request,"rendezvous/readRDv.html",context)


def MesPatient(request):
    patient = RendezVous.objects.filter(medecin=request.user.medecin,status ='CONFIRME')
    context ={
        'patient':patient,
    }
    return render(request,"patient/consulte.html",context)

#Fonctions pour afficher les rendez vous du patient 
def MaRendezVous(request):
    myRDV = RendezVous.objects.filter(patient=request.user.patient)
    context = {
        'myRDV':myRDV,
    }
    return render(request,"rendezvous/myrdv.html",context)

@login_required
def confirmer_rendezvous(request, rendezvous_id):
    rendezvous = get_object_or_404(RendezVous, id=rendezvous_id)
    if request.user.is_medecin:
        rendezvous.status = 'CONFIRME'
        
        Notifications.objects.create(
            user=rendezvous.patient,
            message=f"Votre rendez-vous avec Dr. {rendezvous.medecin.prenom} {rendezvous.medecin.nom} a été confirmé."
        )
        rendezvous.save()
    return redirect('mesrdv')


@login_required
def reject_rendezvous(request, rendezvous_id):
    rendezvous = get_object_or_404(RendezVous, id=rendezvous_id)
    if request.user.is_medecin:
        rendezvous.status = 'ANNULE'
        #envoyer une notification au patient et au médecin
        Notifications.objects.create(
            user=rendezvous.medecin,
            message=f"Le rendez-vous avec {rendezvous.patient.prenom} {rendezvous.patient.nom} a été annulé."
        )
        Notifications.objects.create(
            user=rendezvous.patient,
            message=f"Votre rendez-vous avec Dr. {rendezvous.medecin.prenom} {rendezvous.medecin.nom} a été annulé."
        )
        rendezvous.save()
    return redirect('mesrdv')

def Tableau_de_Bord(request,medecin_id):
    medecin= get_object_or_404(Medecin,id=medecin_id)
    total_rendezvous = RendezVous.objects.filter(medecin=medecin).count()
    total_confirmed_rendezvous = RendezVous.objects.filter(medecin=medecin, status='CONFIRME').count()
    total_cancelled_rendezvous = RendezVous.objects.filter(medecin=medecin, status='ANNULE').count()
    
    context = {
        'total_rendezvous': total_rendezvous,
        'total_confirmed_rendezvous': total_confirmed_rendezvous,
        'total_cancelled_rendezvous': total_cancelled_rendezvous,
    }
    return render(request,"home.html",context)
from django.db.models import Count
from django.utils.timezone import now
from django.db.models.functions import ExtractMonth

import json
import calendar

def dashboard(request):
    status_T = RendezVous.objects.all().count()
    status_C = RendezVous.objects.filter(status='CONFIRME').count()
    status_A = RendezVous.objects.filter(status='ANNULE').count()
    status_E = RendezVous.objects.filter(status='EN_ATTENTE').count()
    
    total_rendezvous = RendezVous.objects.all().count()
    total_medecin = Medecin.objects.all().count()
    total_patient = RendezVous.objects.all().count()
    
    current_year = now().year
    appointments_by_month = RendezVous.objects.filter(programme__date__year=current_year).annotate(month=ExtractMonth('programme__date')).values('month').annotate(count=Count('id')).order_by('month')
    
    month_labels = []
    appointment_counts = []

    for appointment in appointments_by_month:
        month_labels.append(calendar.month_name[appointment['month']])
        appointment_counts.append(appointment['count'])
        
   
    genre_counts = Patient.objects.values('genre').annotate(total=Count('genre')).order_by('genre')
    genre_counts = json.dumps(list(genre_counts), default=str)

   
    bar = [status_T,status_A,status_C,status_E]
    chart_data = {
        'labels': month_labels,
        'data': appointment_counts,
        'bar':bar,
        'total_rendezvous':total_rendezvous,
        'total_medecin':total_medecin,
        'total_patient':total_patient,
        'genre_counts': genre_counts,
    }

    return render(request, "Graphe/dashboard.html", chart_data)

