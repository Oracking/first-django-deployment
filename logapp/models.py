from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentUser(models.Model):
    user = models.OneToOneField(User)
    student_id = models.IntegerField(unique=True, blank = False)
    has_voted = models.BooleanField(default = False)

    def __str__(self):
        return str(self.user)

class Candidate(models.Model):
    candidate = models.OneToOneField(User)
    number_of_votes = models.IntegerField(default = 0)
    manifesto = models.TextField(blank=True)

    def __str__(self):
        return str(self.candidate)
