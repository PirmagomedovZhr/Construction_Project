from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from .models import Task
from .forms import SignUpForm, SignInForm



class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'main/signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    tasks = Task.objects.all()
    return render(request, 'main/index.html',{'tasks':tasks})

def about(request):
    return render(request, 'main/about.html')



def form(request):
    if request.method == 'POST':
        lname = request.POST.get('lname')
        fname = request.POST.get('fname')
        print(lname, fname)
        Task.objects.create(title=lname, task=fname)
        return redirect('/')
    print(request.method)
    return render(request, 'main/form.html')



