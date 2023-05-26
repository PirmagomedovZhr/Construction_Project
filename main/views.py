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
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect


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
    # Exclude archived projects from the projects assigned to the user
    projects = ProjectUser.objects.filter(user=user, project__is_archived=False)
    position = user.get_position_display()
    # Exclude archived projects from the available projects
    available_projects = Project.objects.exclude(is_archived=True)

    if request.method == 'POST':
        project_id = request.POST.get('project')
        user_id = request.POST.get('user')
        due_date = request.POST.get('due_date')

        user = User.objects.get(id=user_id)
        project = Project.objects.get(id=project_id)

        # Check if the project is archived before assigning
        if project.is_archived:
            messages.error(request, 'This project is archived and cannot be assigned')
        else:
            project_user, created = ProjectUser.objects.get_or_create(
                user=user,
                project=project,
                defaults={'due_date': due_date}
            )

            if created:
                messages.success(request, 'Project has been assigned')
            else:
                messages.info(request, 'This project is already assigned to this user')

    return render(request, 'main/user_projects.html', {
        'user': user,
        'position': position,
        'projects': projects,
        'available_projects': available_projects
    })


def projects(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            template = 'main/admin/projects.html'
            return render(request, template, {'projects': Project.objects.all()})
        else:
            return HttpResponseRedirect('/signin')  # редирект не авторизованных пользователей на страницу входа


def deletes_project(request, project_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            project = get_object_or_404(Project, id=project_id)
            project.delete()
            return redirect('projects')
        else:
            return HttpResponseRedirect('/signin')  # редирект не авторизованных пользователей на страницу входа




@login_required
def add_time(request, project_id):
    project_user = get_object_or_404(ProjectUser, project_id=project_id, user=request.user)
    if project_user.due_date < date.today():
        messages.error(request, 'Due date for this project has passed. You cannot add more time.')
        return redirect('base')
    project = Project.objects.get(id=project_id)
    user = request.user
    existing_entry = TimeSpent.objects.filter(Q(user=user) & Q(project=project) & Q(date=date.today()))
    if existing_entry.exists():
        messages.error(request, 'You have already added time for this project today.')
        return redirect('base')
    if request.method == 'POST':
        hours = request.POST['hours']
        description = request.POST['description']
        time_spent = TimeSpent(project=project, user=user, hours_spent=hours, date=date.today(), description=description)
        time_spent.save()
        messages.success(request, 'Time added successfully!')
        return redirect('base')
    else:
        context = {'project': project}
        return render(request, 'main/add_time.html', context)





from django.db.models import Sum

from django.db.models import Window, Sum

def time_spent_list(request):
    time_spent_reports = TimeSpent.objects.select_related('user', 'project').annotate(
        all_hours=Window(
            expression=Sum('hours_spent'),
            partition_by=['user', 'project'],
            order_by=['date']
        )
    ).order_by('date')

    # Handle filters
    user_filter = request.GET.get('user_filter', None)
    project_filter = request.GET.get('project_filter', None)

    if user_filter:
        time_spent_reports = time_spent_reports.filter(user__username=user_filter)

    if project_filter:
        time_spent_reports = time_spent_reports.filter(project__title=project_filter)

    users = User.objects.all()
    projects = Project.objects.all()

    context = {'time_spent_reports': time_spent_reports, 'users': users, 'projects': projects}
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
            return render(request, template, {'tasks': Project.objects.filter(is_archived=False)})
        else:
            return render(request, 'main/users/base.html', {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})

@require_POST
def delete_project(request, projectuser_id):
    projectuser = get_object_or_404(ProjectUser, id=projectuser_id)
    user_id = projectuser.user.id
    projectuser.delete()
    return redirect('user_projects', user_id=user_id)



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


def projectt_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    time_entries = TimeSpent.objects.filter(user=user, project=project)

    context = {
        'project': project,
        'time_entries': time_entries,
    }

    return render(request, 'main/projectt_detail.html', context)


def project_reports(request, project_id):
    reports = TimeSpent.objects.filter(project__id=project_id)
    return render(request, 'main/project_reports.html', {'reports': reports})


def archive_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.is_archived = True
    project.save()
    return redirect('base')

def archive(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/signin')
    else:
        if request.user.is_superuser:
            template = 'main/archived_projects.html'
            return render(request, template, {'tasks': Project.objects.filter(is_archived=True)})
        else:
            return render(request, 'main/archived_projects.html', {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=True)})


def archived_projects(request):
    # Get all archived projects
    tasks = Project.objects.filter(is_archived=True)

    # Render the template with the projects
    return render(request, 'main/archived_projects.html', {'tasks': tasks})


def project_treports(request, project_id):
    project_reports = TimeSpent.objects.filter(project_id=project_id).select_related('user').annotate(
        all_hours=Window(
            expression=Sum('hours_spent'),
            partition_by=['user'],
            order_by=['date']
        )
    ).order_by('date')

    context = {'project_reports': project_reports}
    return render(request, 'main/archive_project_reports.html', context)
