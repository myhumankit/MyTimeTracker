from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from projects.models import Activity, Leave, Project


class ProjectListView(LoginRequiredMixin, ListView):

    model = Project


class ActivityListView(LoginRequiredMixin, ListView):

    model = Activity
    paginate_by = 50

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        return queryset


class LeaveListView(LoginRequiredMixin, ListView):

    model = Leave

    def get_queryset(self):
        queryset = Leave.objects.filter(user=self.request.user)
        return queryset
