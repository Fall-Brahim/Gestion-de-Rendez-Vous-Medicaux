# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import pre_save
from django.dispatch import receiver
from enum import Enum
# Enums
class GenreEnum(Enum):
    MASCULIN = "Masculin"
    FEMININ = "Feminin"


class SpecialiteEnum(Enum):
    GENERALISTE = "Généraliste"
    CARDIOLOGUE = "Cardiologue"
    DERMATOLOGUE = "Dermatologue"
    GYNECOLOGUE = "Gynécologue"
    NEUROLOGUE = "Neurologue"
    OPHTALMOLOGUE = "Ophtalmologue"
    ORL = "ORL"
    PEDIATRE = "Pédiatre"
    PSYCHIATRE = "Psychiatre"
    RADIOLOGUE = "Radiologue"
    CHIRURGIEN = "Chirurgien"
# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nom, prenom, password=None):
        if not email:
            raise ValueError("Le champ Email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, nom=nom, prenom=prenom)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nom, prenom, password=None):
        user = self.create_user(email, nom, prenom, password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

# Abstract Utilisateur Model
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=160)
    email = models.EmailField(max_length=120, unique=True)
    profil = models.ImageField(upload_to='profil_dir', null=True, blank=True)
    genre = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in GenreEnum])
   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    class Meta:
        abstract = False

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_medecin(self):
        return hasattr(self, 'medecin')

    @property
    def is_patient(self):
        return hasattr(self, 'patient')
    
from datetime import date
# Patient Model
class Patient(Utilisateur):
    numero_telephone = models.CharField(max_length=13)
    adresse = models.CharField(max_length=30)
    date_naissance = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @property
    def age(self):
        today = date.today()
        if self.date_naissance:
            return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))
        return None

# Medecin Model
class Medecin(Utilisateur):
    specialite = models.CharField(max_length=70, choices=[(tag.name, tag.value) for tag in SpecialiteEnum], blank=True, null=True)
    informations_contact = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Medecin"
        verbose_name_plural = "Medecins"

    def __str__(self):
        return f"Dr. {self.prenom} {self.nom}"
from django.utils import timezone
# Notifications Model
class Notifications(models.Model):
    user = models.ForeignKey(Utilisateur, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    envoyee = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.id} - {self.user}"