from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from .models import Task
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



