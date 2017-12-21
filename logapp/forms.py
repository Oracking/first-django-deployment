from django import forms
from django.contrib.auth.models import User
from .models import StudentUser, Candidate


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'email',)


class StudentUserForm(forms.ModelForm):
    class Meta:
        model = StudentUser
        fields = ('student_id',)

class VoteForm(forms.Form):
    candidate = forms.ModelChoiceField(queryset=Candidate.objects.all())
