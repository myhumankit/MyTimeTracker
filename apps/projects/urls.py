from django.urls import path

from projects.views import (
    ActivityListView,
    LeaveListView,
    ProjectListView,
    ProjectListByUserView,
    ProjectDetailView,
    ProjectDetailByUserView,
)

app_name = "projects"
urlpatterns = [
    path("", ActivityListView.as_view(), name="activity_list"),
    path("projects", ProjectListView.as_view(), name="project_list"),
    path(
        "projects/user/<str:username>/",
        ProjectListByUserView.as_view(),
        name="project_list_by_user",
    ),
    path("projects/<uuid:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path(
        "projects/<uuid:pk>/user/<str:username>/",
        ProjectDetailByUserView.as_view(),
        name="project_detail_by_user",
    ),
    path("absences", LeaveListView.as_view(), name="leave_list"),
]
