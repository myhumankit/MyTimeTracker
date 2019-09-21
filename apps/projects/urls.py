from django.urls import path

from projects.views import TaskListView

urlpatterns = [path("", TaskListView.as_view(), name="task-list")]
