from datetime import date
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Project
from .forms import SignUpForm, SignInForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.views import View
from .models import User, ProjectUser, TimeSpent
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def login(request):
     context = {}
     request_context = RequestContext(request)
     return render_to_response('main/admin/base.html', context,
                               request_context=request_context)


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



@login_required
def add_time(request, project_id):
    project = Project.objects.get(id=project_id)
    user = request.user
    existing_entry = TimeSpent.objects.filter(Q(user=user) & Q(project=project) & Q(date=date.today()))
    if existing_entry.exists():
        messages.error(request, 'You have already added time for this project today.')
        return redirect('base')
    if request.method == 'POST':
        hours = request.POST['hours']
        time_spent = TimeSpent(project=project, user=user, hours_spent=hours, date=date.today())
        time_spent.save()
        messages.success(request, 'Time added successfully!')
        return redirect('base')
    else:
        context = {'project': project}
        return render(request, 'main/add_time.html', context)



def time_spent_list(request):
    time_spent = TimeSpent.objects.order_by('date')
    time_spent_dict = {}

    for entry in time_spent:
        date = entry.date
        user = entry.user
        hours_spent = entry.hours_spent
        if date not in time_spent_dict:
            time_spent_dict[date] = {}
        if user not in time_spent_dict[date]:
            time_spent_dict[date][user] = 0
        time_spent_dict[date][user] += hours_spent


    time_spent_list = []
    for date, user_hours_dict in time_spent_dict.items():
        for user, hours in user_hours_dict.items():
            time_spent_list.append((date, user, hours))

    context = {'time_spent_list': time_spent_list}
    return render(request, 'main/time_spent_list.html', context)




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
            if request.user.is_superuser:

                return render(request, 'main/users/base.html', {'tasks': Project.objects.all()})
            else:
                return render(request, 'main/users/base.html', {'projects': ProjectUser.objects.filter(user=request.user)})
        else:
            return render(request, 'main/signup.html', context={
                'form': SignUpForm(),
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
            if request.user.is_superuser:
                tasks = Project.objects.all()
                return render(request, 'main/users/base.html', {'tasks': tasks})
            else:
                return render(request, 'main/users/base.html',
                              {'projects': ProjectUser.objects.filter(user=request.user)})
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
            return render(request, template, {'tasks': Project.objects.all()})
        else:
            return render(request, 'main/users/base.html', {'projects': ProjectUser.objects.filter(user=request.user)})



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
        return render(request, 'main/users/base.html', {'projects': ProjectUser.objects.filter(user=request.user)})
    else:
        return HttpResponseRedirect('/signin')


def logout_user(request):
    logout(request)
    return redirect('signin')


