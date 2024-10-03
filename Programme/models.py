from django.db import models
from Users.models import Medecin

class Programme(models.Model):
    JOUR_CHOICES = [
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'),
        ('Vendredi', 'Vendredi'),
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
    ]

    MOIS_CHOICES = [
        ('Janvier', 'Janvier'),
        ('Février', 'Février'),
        ('Mars', 'Mars'),
        ('Avril', 'Avril'),
        ('Mai', 'Mai'),
        ('Juin', 'Juin'),
        ('Juillet', 'Juillet'),
        ('Août', 'Août'),
        ('Septembre', 'Septembre'),
        ('Octobre', 'Octobre'),
        ('Novembre', 'Novembre'),
        ('Décembre', 'Décembre'),
    ]

    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE,editable=False)
    jour = models.CharField(max_length=10, choices=JOUR_CHOICES)
    mois = models.CharField(max_length=10, choices=MOIS_CHOICES)
    date = models.DateField()
    debut_heure = models.TimeField()
    fin_heure = models.TimeField()

    def __str__(self):
        return f"{self.jour} {self.date} - {self.medecin.nom} {self.medecin.prenom}"

    def clean(self):
        if self.debut_heure >= self.fin_heure:
            raise ValidationError('L\'heure de début doit être avant l\'heure de fin')

    class Meta:
        verbose_name = 'Programme'
        verbose_name_plural = 'Programmes'
        ordering = ['medecin', 'date', 'debut_heure']
