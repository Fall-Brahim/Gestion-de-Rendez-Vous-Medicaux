#views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProgrammeForm
from .models import Programme
from Users.models import Medecin


@login_required
def programme(request):
    if request.method == "POST":
        form = ProgrammeForm(request.POST)
        if form.is_valid():
            programme = form.save(commit=False)
            programme.medecin = request.user.medecin  # Since we know request.user is a Medecin
            programme.save()
            #messages.success(request, "Programme créé avec succès.")
            return redirect('programme')
    else:
        form = ProgrammeForm()
        
    context = {
        'form': form
    }
    return render(request, "programme/timeManager.html", context)


@login_required
def EmploiDuTemps(request):
    emploi = Programme.objects.filter(medecin = request.user.medecin)
    context = {
        'emploi':emploi,
    }
    return render(request,"programme/EmploiTemps.html",context)
