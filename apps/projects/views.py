from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from projects.models import Activity, Leave, Project


class ProjectListView(LoginRequiredMixin, ListView):

    model = Project


class ActivityListView(LoginRequiredMixin, ListView):

    model = Activity
    paginate_by = 50


class LeaveListView(LoginRequiredMixin, ListView):

    model = Leave
