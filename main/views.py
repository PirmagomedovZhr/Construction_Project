from datetime import date
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Project
from .forms import SignUpForm, SignInForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.views import View
from .models import User, ProjectUser, TimeSpent
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Window, Sum
from django.utils.decorators import method_decorator

def is_admin(user):
    return user.is_authenticated and user.is_superuser

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


class UserListView(View):
    template_superuser = 'main/user_list.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                users = User.objects.filter(is_active=True)
                return render(request, self.template_superuser, {'users': users})
            else:
                projects = ProjectUser.objects.filter(user=request.user, project__is_archived=False)
                return render(request, self.template_user, {'projects': projects})
        else:
            return HttpResponseRedirect(self.redirect_url)



class UserProjectsView(View):
    template_superuser = 'main/user_projects.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request, user_id):
        if request.user.is_superuser:
            user = get_object_or_404(User, id=user_id)
            projects = ProjectUser.objects.filter(user=user, project__is_archived=False)
            position = user.get_position_display()
            available_projects = Project.objects.exclude(is_archived=True)

            return render(request, self.template_superuser, {
                'user': user,
                'admin_user': request.user,
                'position': position,
                'projects': projects,
                'available_projects': available_projects
            })
        else:
            return render(request, self.template_user, {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})

    def post(self, request, user_id):
        if request.user.is_superuser:
            project_id = request.POST.get('project')
            user_id = request.POST.get('user')
            due_date = request.POST.get('due_date')

            user = get_object_or_404(User, id=user_id)
            project = get_object_or_404(Project, id=project_id)

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

            return HttpResponseRedirect(request.path)

        return HttpResponseRedirect(self.redirect_url)



class ProjectsView(View):
    template_superuser = 'main/admin/projects.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request):
        if request.user.is_superuser:
            return render(request, self.template_superuser, {'projects': Project.objects.all()})
        elif request.user.is_authenticated:
            return render(request, self.template_user,
                          {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect(self.redirect_url)



class DeletesProjectView(View):
    redirect_url = '/signin'

    def post(self, request, project_id):
        if request.user.is_superuser:
            project = get_object_or_404(Project, id=project_id)
            project.delete()
            return redirect('projects')
        else:
            return HttpResponseRedirect(self.redirect_url)




class AddTimeView(View):
    template_user = 'main/users/add_time.html'
    redirect_url = '/signin'

    def get(self, request, project_id):
        if request.user.is_superuser:
            template = 'main/admin/base.html'
            return render(request, template, {'tasks': Project.objects.filter(is_archived=False)})
        else:
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
            context = {'project': project}
            return render(request, self.template_user, context)

    def post(self, request, project_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return HttpResponseRedirect(self.redirect_url)
            else:
                project = get_object_or_404(Project, id=project_id)
                user = request.user
                existing_entry = TimeSpent.objects.filter(Q(user=user) & Q(project=project) & Q(date=date.today()))
                if existing_entry.exists():
                    messages.error(request, 'You have already added time for this project today.')
                    return redirect('base')
                hours = request.POST['lname']
                description = request.POST['fname']
                time_spent = TimeSpent(project=project, user=user, hours_spent=hours, date=date.today(), description=description)
                time_spent.save()
                messages.success(request, 'Time added successfully!')
                return redirect('base')
        else:
            return HttpResponseRedirect(self.redirect_url)



class TimeSpentListView(View):
    template_superuser = 'main/time_spent_list.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                time_spent_reports = TimeSpent.objects.select_related('user', 'project').annotate(
                    all_hours=Window(
                        expression=Sum('hours_spent'),
                        partition_by=['user', 'project'],
                        order_by=['date']
                    )
                ).order_by('date')

                user_filter = request.GET.get('user_filter', None)
                project_filter = request.GET.get('project_filter', None)

                if user_filter:
                    time_spent_reports = time_spent_reports.filter(user__username=user_filter)

                if project_filter:
                    time_spent_reports = time_spent_reports.filter(project__title=project_filter)

                # Filter out time spent on archived projects
                time_spent_reports = time_spent_reports.filter(project__is_archived=False)

                users = User.objects.all()
                projects = Project.objects.filter(is_archived=False)  # Only non-archived projects

                context = {'time_spent_reports': time_spent_reports, 'users': users, 'projects': projects}
                return render(request, self.template_superuser, context)
            else:
                return render(request, self.template_user,
                              {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect(self.redirect_url)



class GetUserView(View):
    template_superuser = 'main/admin/users.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, self.template_superuser, {'users': User.objects.filter(is_active=True)})
            else:
                tasks = Project.objects.all()
                return render(request, self.template_user, {'tasks': tasks})
        else:
            return HttpResponseRedirect(self.redirect_url)



class ActivateUserView(View):
    redirect_url = '/signin'

    def post(self, request, user_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                user = User.objects.get(pk=user_id)
                user.is_active = True
                user.save()
                return redirect('activate')
            else:
                tasks = Project.objects.all()
                return render(request, 'main/users/base.html', {'tasks': tasks})
        else:
            return HttpResponseRedirect(self.redirect_url)



class InactiveUsersView(View):
    template_superuser = 'main/admin/activate.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                inactive_users = User.objects.filter(is_active=False)
                context = {'inactive_users': inactive_users}
                return render(request, self.template_superuser, context)
            else:
                tasks = Project.objects.all()
                return render(request, self.template_user, {'tasks': tasks})
        else:
            return HttpResponseRedirect(self.redirect_url)


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, 'main/admin/base.html', {'tasks': Project.objects.all()})
            else:
                return render(request, 'main/users/base.html', {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return render(request, 'main/signup.html', context={
                'form': SignUpForm(),
        })


    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main/signin.html', context={
                'form': form,
            })
        return render(request, 'main/signup.html', context={
            'form': form,
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                tasks = Project.objects.all()
                return render(request, 'main/admin/base.html', {'tasks': tasks})
            else:
                return render(request, 'main/users/base.html',
                              {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
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


class BaseView(View):
    template_superuser = 'main/admin/base.html'
    template_user = 'main/users/base.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, self.template_superuser, {'tasks': Project.objects.filter(is_archived=False)})
            else:
                return render(request, self.template_user, {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect('/signin')




class DeleteProjectView(View):
    redirect_url = '/signin'

    def post(self, request, projectuser_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                projectuser = get_object_or_404(ProjectUser, id=projectuser_id)
                user_id = projectuser.user.id
                projectuser.delete()
                return redirect('user_projects', user_id=user_id)
            else:
                return render(request, 'main/users/base.html', {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect(self.redirect_url)


class FormView(View):
    template_superuser = 'main/form.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request):
        if request.user.is_superuser:
            return render(request, self.template_superuser)
        elif request.user.is_authenticated:
            return render(request, self.template_user, {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect(self.redirect_url)

    def post(self, request):
        if request.user.is_superuser:
            lname = request.POST.get('lname')
            fname = request.POST.get('fname')

            if len(lname) > 4 or len(fname) > 4:
                Project.objects.create(title=lname, task=fname)
                return redirect('/')
        return render(request, self.template_superuser)



class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('signin')



class ProjectDetailsView(View):
    template_user = 'main/users/project_detail_for_user.html'
    redirect_url = '/signin'

    def get(self, request, project_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                template = 'main/admin/base.html'
                return render(request, template, {'tasks': Project.objects.filter(is_archived=False)})
            else:
                project = get_object_or_404(Project, id=project_id)
                user = request.user
                time_entries = TimeSpent.objects.filter(user=user, project=project)

                context = {
                    'project': project,
                    'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False),
                    'time_entries': time_entries,
                }

                return render(request, self.template_user, context)
        else:
            return HttpResponseRedirect(self.redirect_url)



class ProjectReportsView(View):
    template_superuser = 'main/project_reports.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request, project_id):
        if request.user.is_superuser:
            reports = TimeSpent.objects.filter(project__id=project_id)
            return render(request, self.template_superuser, {'reports': reports, 'project': get_object_or_404(Project, id=project_id)})
        else:
            return render(request, self.template_user, {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})



class ArchiveProjectView(View):
    redirect_url = '/signin'

    def post(self, request, project_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                project = Project.objects.get(id=project_id)
                project.is_archived = True
                project.save()
                return redirect('base')
            else:
                return render(request, 'main/users/base.html', {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect(self.redirect_url)



class ArchiveView(View):
    template_superuser = 'main/archived_projects.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return render(request, self.template_superuser, {'tasks': Project.objects.filter(is_archived=True)})
            else:
                return render(request, self.template_user, {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect(self.redirect_url)



class ProjectTReportsView(View):
    template_superuser = 'main/archive_project_reports.html'
    template_user = 'main/users/base.html'
    redirect_url = '/signin'

    def get(self, request, project_id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                project_reports = TimeSpent.objects.filter(project_id=project_id).select_related('user').annotate(
                    all_hours=Window(
                        expression=Sum('hours_spent'),
                        partition_by=['user'],
                        order_by=['date']
                    )
                ).order_by('date')

                context = {'project': get_object_or_404(Project, id=project_id),
                           'project_reports': project_reports}
                return render(request, self.template_superuser, context)
            else:
                return render(request, self.template_user, {'projects': ProjectUser.objects.filter(user=request.user, project__is_archived=False)})
        else:
            return HttpResponseRedirect(self.redirect_url)



