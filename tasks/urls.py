from django.urls import path
from tasks.views import home, login_view, add_task, filter_tasks, update_task, delete_task, register_view, logout_view

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("add_task/", add_task, name="add_task"),
    path("tasks/<str:foo>/", filter_tasks, name="tasks"),
    path("task/<int:pk>/", update_task, name="task"),
    path("task/<int:pk>/", delete_task, name="delete"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout")
]