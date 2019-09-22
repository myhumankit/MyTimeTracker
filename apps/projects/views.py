from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from projects.models import Project


class ProjectListView(LoginRequiredMixin, ListView):

    model = Project
    paginate_by = 5
