from django.db import models
from Users.models import Medecin,Patient
from enum import Enum
from Programme.models import Programme
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Users.models import Notifications

class StatusRDVEnum(Enum):
    CONFIRME = "Confirme"
    ANNULE = "Annuler"
    EN_ATTENTE = "En Attente"
    REPORTER = "Reporter"

# Create your models here.
# RendezVous Model
class RendezVous(models.Model):
    programme = models.ForeignKey(Programme,related_name="programme",on_delete=models.CASCADE,editable=False)
    patient = models.ForeignKey(Patient, related_name='rendez_vous', on_delete=models.CASCADE, editable=False)
    medecin = models.ForeignKey(Medecin, related_name='rendez_vous', on_delete=models.CASCADE)
    confirmation = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in StatusRDVEnum], default='EN_ATTENTE')
    motif = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"RDV {self.id} - {self.patient.nom} avec {self.medecin.nom}"


# Signals
@receiver(post_save, sender=RendezVous)
def send_notification_on_create_or_update(sender, instance, created, **kwargs):
    if created:
        # Notification to Medecin when a new RendezVous is created
        Notifications.objects.create(
            users=instance.medecin,
            message=f"Vous avez un nouveau rendez-vous avec {instance.patient.prenom} {instance.patient.nom}."
        )
    else:
        # Notification to Patient when the RendezVous is confirmed
        if instance.confirmation:
            Notifications.objects.create(
                users=instance.patient,
                message=f"Votre rendez-vous avec Dr. {instance.medecin.prenom} {instance.medecin.nom} a été confirmé."
            )

@receiver(post_delete, sender=RendezVous)
def send_notification_on_delete(sender, instance, **kwargs):
    # Notification to Medecin and Patient when the RendezVous is canceled
    Notifications.objects.create(
        users=instance.medecin,
        message=f"Le rendez-vous avec {instance.patient.prenom} {instance.patient.nom} a été annulé."
    )
    Notifications.objects.create(
        users=instance.patient,
        message=f"Votre rendez-vous avec Dr. {instance.medecin.prenom} {instance.medecin.nom} a été annulé."
    )