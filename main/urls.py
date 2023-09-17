from django.urls import path
from .views import (UserListView, UserProjectsView, ProjectsView, DeletesProjectView, TimeSpentListView, AddTimeView, GetUserView, ActivateUserView, InactiveUsersView,
                    LogoutUserView, ProjectDetailsView, FormView, DeleteProjectView, BaseView, ProjectReportsView, ArchiveProjectView, ArchiveView, ProjectTReportsView, SignInView, SignUpView)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),#Главная
    path('form/', FormView.as_view(), name='form'),
    path('signup/', SignUpView.as_view(), name='signup'),#Регистрация
    path('signin/', SignInView.as_view(), name='signin'),#Авторизация
    path('logout/', LogoutUserView.as_view(), name='logout'),#Выход
    path('activate/', InactiveUsersView.as_view(), name='activate'),#Страница активаций аккаунтов пользователей
    path('activate_user/<int:user_id>/', ActivateUserView.as_view(), name='activate_user'),#Активация аккаунта пользователя
    path('use/', GetUserView.as_view(), name='use'),
    path('users/', UserListView.as_view(), name='user_list'),#Управление проектами
    path('user_projects/<int:user_id>/', UserProjectsView.as_view(), name='user_projects'),#Назначение и удаление проектов у пользователя
    path('delete_project/<int:projectuser_id>/', DeleteProjectView.as_view(), name='delete_project'),
    path('add_time/<int:project_id>/', AddTimeView.as_view(), name='add_time'),#Добавление времени к проекту у пользователя(отчет)
    path('timespent/', TimeSpentListView.as_view(), name='timespent'),#Список отчетов
    path('delete_project_for_user/<int:project_id>/', DeletesProjectView.as_view(), name='delete_project_for_user'),
    path('projects/', ProjectsView.as_view(), name='projects'),# Удаление проектов
    path('projectt/<int:project_id>/', ProjectDetailsView.as_view(), name='projectt_details'),#Подробная информация о выбранном проекте
    path('project-reports/<int:project_id>/', ProjectReportsView.as_view(), name='project_reports'),
    path('projectttt/<int:project_id>/archive/', ArchiveProjectView.as_view(), name='archive_project'),
    path('archived_projects/', ArchiveView.as_view(), name='archived_projects'),#Архив проектов
    path('archive/project_reports/<int:project_id>/', ProjectTReportsView.as_view(), name='archive_project_reports'),
]