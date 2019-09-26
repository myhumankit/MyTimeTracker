from django.urls import path

from projects.views import (
    ActivityListView,
    LeaveListView,
    ProjectListView,
    ProjectDetailView,
)

app_name = "projects"
urlpatterns = [
    path("", ActivityListView.as_view(), name="activity_list"),
    path("projects", ProjectListView.as_view(), name="project_list"),
    path("projects/<uuid:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("absences", LeaveListView.as_view(), name="leave_list"),
]
