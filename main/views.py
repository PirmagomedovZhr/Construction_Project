from django.http import HttpResponseRedirect
from .models import Task
from .forms import SignUpForm, SignInForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.views import View
from .models import User, ProjectUser


def add_user_to_project(project, user):
    project_user = ProjectUser(project=project, user=user)
    project_user.save()

def remove_user_from_project(project, user):
    project_user = ProjectUser.objects.get(project=project, user=user)
    project_user.delete()

def clear_project_users(project):
    ProjectUser.objects.filter(project=project).delete()



def get_users_by_position(position):
    return User.objects.filter(position=position)






def lindex(request):
    users = User.objects.all()
    data = []
    for user in users:
        projects = ProjectUser.objects.filter(user=user).values_list('project__title', flat=True)
        position = user.get_position_display()
        data.append({'user': user.username, 'position': position, 'projects': ', '.join(projects)})
    return render(request, 'main/lll.html', {'data': data})



def kkk(request):
    users = User.objects.all()
    tasks = Task.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        task_id = request.POST.get('task')
        user = User.objects.get(id=user_id)
        task = Task.objects.get(id=task_id)
        ProjectUser.objects.create(user=user, project=task)
        return redirect('kkk')

    return render(request, 'main/kkk.html', {'users': users, 'tasks': tasks})



















def Get_User(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            return render(request, 'main/admin/users.html', {'users': User.objects.filter(is_active=True)})
        else:
            tasks = Task.objects.all()
            return render(request, 'main/users/base.html', {'tasks': tasks})


def activate_user(request, user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            user = User.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            return redirect('activate')
        else:
            tasks = Task.objects.all()
            return render(request, 'main/users/base.html', {'tasks': tasks})


def inactive_users(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            inactive_users = User.objects.filter(is_active=False)
            context = {'inactive_users': inactive_users}
            return render(request, 'main/admin/activate.html', context)
        else:
            tasks = Task.objects.all()
            return render(request, 'main/users/base.html', {'tasks': tasks})



class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tasks = Task.objects.all()
            return render(request, 'main/users/base.html', {'tasks': tasks})
        else:
            form = SignUpForm()
            return render(request, 'main/signup.html', context={
                'form': form,
        })


    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        return render(request, 'main/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tasks = Task.objects.all()
            return render(request, 'main/users/base.html', {'tasks': tasks})
        else:
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



def base(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            template = 'main/admin/base.html'
        else:
            template = 'main/users/base.html'
        tasks = Task.objects.all()
        return render(request, template, {'tasks':tasks})


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
        return render(request, 'main/users/base.html', {'tasks': tasks})
    else:
        return HttpResponseRedirect('/signin')


def logout_user(request):
    logout(request)
    return redirect('signin')


