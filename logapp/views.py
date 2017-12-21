from django.shortcuts import render
from .forms import UserForm, StudentUserForm, VoteForm
from .models import StudentUser, Candidate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.user.is_authenticated:
        return render(request, 'logapp/request_logout.html')

    else:
        if request.method == 'POST':
            #If user has sent login details
            student_id = request.POST.get('user_id')
            query = StudentUser.objects.filter(student_id = student_id)

            if len(query) == 1:
                username = query[0].user.username
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)

                if user is not None:

                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('index'))
                    else:
                        return HttpResponse('Your account is inactive. Contact administration to reactivate your account')
            return HttpResponse('The details that you entered are invalid. Please check and try again.')

        else:
            #If user is now requesting for log in page
            return render(request, 'logapp/user_login.html')

def user_register(request):
    if request.user.is_authenticated:
        #If a user is already logged in
        return render(request, 'logapp/request_logout.html')

    else:
        user_form = UserForm(prefix='user')
        student_user_form = StudentUserForm(prefix='student_user')
        #If a user is not already logged in
        if request.method == 'POST':
            user_form = UserForm(request.POST, prefix='user')
            student_user_form = StudentUserForm(request.POST, prefix='student_user')

            if user_form.is_valid() and student_user_form.is_valid():
                user = user_form.save(commit=False)

                #UserName = First Name + Last Name
                name = user.first_name.strip() + ' ' + user.last_name.strip()
                user.username = name
                user.set_password(user.password)
                user.save()
                student_user = student_user_form.save(commit=False)
                student_user.user = user
                student_user.save()
                return HttpResponseRedirect(reverse('index'))

        return render(request, 'logapp/user_register.html', {'user_form': user_form,
                                                        'student_user_form': student_user_form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('You are already logged out. Do you mean to log in?')

@login_required
def vote(request):
    student_user = StudentUser.objects.get(user = request.user)
    if student_user.has_voted:
        return HttpResponse('You have already voted. Do you wish to change your vote?')
    else:
        vote_form = VoteForm()
        if request.method == 'POST':
            vote_form = VoteForm(request.POST)

            if vote_form.is_valid():
                candidate = vote_form.cleaned_data['candidate']
                candidate.number_of_votes += 1
                candidate.save()
                student_user.has_voted = True
                student_user.save()
                return HttpResponse('Thank You for Voting')

        return render(request, 'logapp/vote.html', {'vote_form': vote_form})
