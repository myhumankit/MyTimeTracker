from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from projects.models import Task


class TaskListView(LoginRequiredMixin, ListView):

    model = Task
    paginate_by = 5
