
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from .models import Task, Profile
from .forms import SignUpForm, SignInForm, ProfileForm
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render
from django.views import View
from .models import User, Profile


class UsersView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        positions = Profile.objects.all()
        print(positions)
        print(users)
        return render(request, 'main/register.html', context={'users': users, 'positions': positions})


def activate_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('active')

def inactive_users(request):
    # Получение всех неактивных пользователей
    inactive_users = User.objects.filter(is_active=False)

    # Передача списка неактивных пользователей в шаблон
    context = {'inactive_users': inactive_users}
    return render(request, 'main/inactive_users.html', context)

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'main/signup.html', context={
            'form': form,
        })


    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            profile = Profile.objects.create(user=user, position=profile_form.cleaned_data['position'])
            profile.save()
            if user is not None:
                return HttpResponseRedirect('/')
        return render(request, 'main/signup.html', context={
            'form': form,
        })

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'main/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'main/signin.html', context={
            'form': form,
        })



def index(request):
    template = ''
    form = SignInForm(request.POST)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            template = 'main/about.html'
        else:
            template = 'main/base.html'
        tasks = Task.objects.all()
        return render(request, template, {'tasks':tasks})

def get_user(request):
    template = ''
    form = SignInForm(request.POST)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            template = 'main/users.html'
        else:
            template = '/'
        users_list = User.objects.filter(is_active=True)
        return render(request, template, {"users_list": users_list},)


def about(request):
    return render(request, 'main/about.html')



def form(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            lname = request.POST.get('lname')
            fname = request.POST.get('fname')

            if len(lname) > 4 or len(fname) > 4:
                Task.objects.create(title=lname, task=fname)
                return redirect('/')
        print(request.method)
        return render(request, 'main/form.html')
    elif request.user.is_authenticated:
        tasks = Task.objects.all()
        return render(request, 'main/base.html', {'tasks': tasks})
    else:
        return HttpResponseRedirect('/signin')


def logout_user(request):
    logout(request)
    return redirect('signin')


