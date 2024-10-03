from django.shortcuts import render,redirect,get_object_or_404
from .models import Medecin,Patient,Notifications
from Rendezvous.models import RendezVous
from Programme.models import Programme
from .forms import RegisterForm,PatientForm,LoginForm,EditePatientForm,EditMedecinForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Rendezvous.models import RendezVous
# Create your views here.
def home(request):
    total_rendezvous = RendezVous.objects.filter().count()
    total_confirmed_rendezvous = RendezVous.objects.filter(status='CONFIRME').count()
    total_cancelled_rendezvous = RendezVous.objects.filter(status='ANNULE').count()
    
    context = {
        'total_rendezvous': total_rendezvous,
        'total_confirmed_rendezvous': total_confirmed_rendezvous,
        'total_cancelled_rendezvous': total_cancelled_rendezvous,
    }
    return render(request,"home.html",context)


def RegisterMedecin(request):
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,"Medecin Inscrit avec succes Veuillez contacter les Admin pour l'activation du compte")
            return redirect('logine')
    else:
        form = RegisterForm()
        
    context = {
        'form':form
    }    
    return render(request,"medecin/register.html",context)


def RegisterPatient(request):
    if request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,"Patient Inscrit avec success")
            return redirect('logine')
    else:
        form = PatientForm()
    
    context = {
        'form':form
    }
    return render(request,"patient/register.html",context)

from django.db.models import Count
import json

@login_required
def all_users(request):
    medecins = Medecin.objects.all()
    patients = Patient.objects.all()

    # Compte des médecins par spécialité
    specialite_counts = Medecin.objects.values('specialite').annotate(total=Count('specialite')).order_by('specialite')
    specialite_counts = json.dumps(list(specialite_counts), default=str)

    context = {
        'medecins': medecins,
        'patients': patients,
        'specialite_counts': specialite_counts
    }
    return render(request,"admin/All_users.html",context)

@login_required
def liste_patiens(request):
    patients = Patient.objects.all()
    context = {
        'patients':patients
    }
    return render(request,"admin/All_patient.html",context)



@login_required
def activate(request,medecin_id):
    medecin = get_object_or_404(Medecin,id=medecin_id)
    medecin.is_verified =not medecin.is_verified
    medecin.save()
    return redirect('all_users')

#Les fonctions d'edite Medecin et de Patient
@login_required
def Editer_Medecin(request):
    medecin = get_object_or_404(Medecin,pk=request.user.medecin)
    if request.method == 'POST':
        form = EditMedecinForm(request.POST,request.FILES, instance=medecin)
        if form.is_valid():
            form.save()
            messages.success(request,"Editer avec success")
            return redirect("doctor_detail",id=medecin.id)
    else:
        form =EditMedecinForm(instance=medecin)
    context = {
        'form':form 
    }
    return render(request,"medecin/edit.html",context)


@login_required
def Editer_Patient(request):
    patient = get_object_or_404(Patient,pk=request.user.patient)
    if request.method == 'POST':
        form = EditePatientForm(request.POST,request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request,"Editer avec success")
            return redirect("patientProf")
    else:
        form =EditePatientForm(instance=patient)
    context = {
        'form':form 
    }
    return render(request,"patient/edit.html",context)




@login_required
def profile_patient(request, Id):
    try:
        patient = get_object_or_404(Patient, id=Id)
        rdv = RendezVous.objects.filter(patient=patient)
        context = {
            'user_type': 'patient',
            'patient': patient,
            'rdv': rdv,
        }
    except:
        medecin = get_object_or_404(Medecin, id=Id)
        rdvmed = RendezVous.objects.filter(medecin=medecin)
        context = {
            'user_type': 'medecin',
            'medecin': medecin,
            'rdvmed': rdvmed,
        }
    
    return render(request, "profile.html", context)


@login_required
def doctors(request):
    doctors = Medecin.objects.filter(is_verified=True)
    context = {
        'doctors':doctors,
    }
    return render(request,"medecin/list.html",context)

@login_required
def doctor_detail(request, id):
    doctor = get_object_or_404(Medecin, id=id)
    programmes = Programme.objects.filter(medecin=doctor)
    context = {
        'doctor': doctor,
        'programmes':programmes
    }
    return render(request, "medecin/detail.html", context)

from .models import Notifications


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notifications, id=notification_id, user=request.user.patient)
    notification.read = True
    notification.save()
    context = {
        'notification': notification
    }
    return render(request, 'notifcations.html', context)


from django.views.decorators.cache import never_cache

@never_cache
def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            # Check if the user is a doctor and if their account is verified
            if hasattr(user, 'medecin') and not user.medecin.is_verified:
                messages.warning(request, "Votre compte de médecin n'est pas encore vérifié.")
            else:
                login(request, user)
                messages.success(request, "Connecté avec succès")
                return redirect('home')
        else:
            messages.error(request, "Échec de connexion, veuillez vérifier vos données")
    
    return render(request, "security/loginForm.html")

@never_cache
@login_required
def LogOut(request):
    logout(request)
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return redirect('home')
