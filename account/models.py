from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # Custom fields for the user model
    contactNo = models.CharField(max_length=15, blank=True, null=True)
    profilePicture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=[
        ('Member', 'Member'),
        ('Team Leader', 'Team Leader'),
        ('Admin', 'Admin')
    ], default='Member', blank=True, null=True)

    # Foreign key to the Team model
    team = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, blank=True, null=True, related_name='members')
    def __str__(self):
        return self.username