from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Project
from .forms import SignUpForm, SignInForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.views import View
from .models import User, ProjectUser

from django.views.generic.list import ListView
from .models import ProjectUser
from django.shortcuts import render, redirect, get_object_or_404


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






def lll(request):
    users = User.objects.all()
    data = []
    for user in users:
        projects = ProjectUser.objects.filter(user=user).values_list('project__title', flat=True)
        position = user.get_position_display()
        data.append({'user': user.username, 'position': position, 'projects': ', '.join(projects)})
    return render(request, 'main/lll.html', {'data': data})



def kkk(request):
    users = User.objects.all()
    tasks = Project.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        task_id = request.POST.get('task')
        user = User.objects.get(id=user_id)
        task = Project.objects.get(id=task_id)
        ProjectUser.objects.create(user=user, project=task)
        return redirect('kkk')

    return render(request, 'main/kkk.html', {'users': users, 'tasks': tasks})



def jjj(request):
    # получаем всех пользователей и проекты
    users = User.objects.all()
    projects = Project.objects.all()

    # обрабатываем отправленную форму
    if request.method == 'POST':
        user_id = request.POST.get('user')
        project_id = request.POST.get('project')

        # ищем запись ProjectUser по выбранным user_id и project_id
        project_user = ProjectUser.objects.filter(user=user_id, project=project_id).first()

        # если такая запись есть, удаляем ее
        if project_user:
            project_user.delete()
            return redirect('jjj')

    # если запрос GET, просто отображаем шаблон
    return render(request, 'main/jjj.html', {'users': users, 'projects': projects})




def user_list(request):
    users = User.objects.all()
    return render(request, 'main/user_list.html', {'users': users})


def user_projects(request, user_id):
    user = User.objects.get(id=user_id)
    projects = ProjectUser.objects.filter(user=user)
    position = user.get_position_display()
    available_projects = Project.objects.all()

    if request.method == 'POST':
        project_id = request.POST.get('project')
        user_id = request.POST.get('user')
        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)
        ProjectUser.objects.create(user=user, project=project)
        messages.success(request, 'Project has been assigned')

    return render(request, 'main/user_projects.html', {
        'user': user,
        'position': position,
        'projects': projects,
        'available_projects': available_projects
    })

def delete_project(request, project_id):
    project = ProjectUser.objects.get(id=project_id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project has been deleted')
        return redirect('user_projects', user_id=project.user.id)
    return redirect('user_projects', user_id=project.user.id)













def Get_User(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            return render(request, 'main/admin/users.html', {'users': User.objects.filter(is_active=True)})
        else:
            tasks = Project.objects.all()
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
            tasks = Project.objects.all()
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
            tasks = Project.objects.all()
            return render(request, 'main/users/base.html', {'tasks': tasks})



class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            tasks = Project.objects.all()
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
            tasks = Project.objects.all()
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
        tasks = Project.objects.all()
        return render(request, template, {'tasks':tasks})


def form(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            lname = request.POST.get('lname')
            fname = request.POST.get('fname')

            if len(lname) > 4 or len(fname) > 4:
                Project.objects.create(title=lname, task=fname)
                return redirect('/')
        print(request.method)
        return render(request, 'main/form.html')
    elif request.user.is_authenticated:
        tasks = Project.objects.all()
        return render(request, 'main/users/base.html', {'tasks': tasks})
    else:
        return HttpResponseRedirect('/signin')


def logout_user(request):
    logout(request)
    return redirect('signin')


